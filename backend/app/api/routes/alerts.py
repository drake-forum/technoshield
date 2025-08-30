from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.core.security import get_current_user
from app.models.user import User
from app.models.alert import Alert
from app.schemas.alert import AlertCreate, AlertResponse, AlertUpdate
from app.core.metrics import record_alert, resolve_alert
from app.db.session import get_db

router = APIRouter()


@router.get("/", response_model=List[AlertResponse])
async def get_alerts(
    severity: Optional[str] = Query(None, description="Filter by severity"),
    status: Optional[str] = Query(None, description="Filter by status"),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db = Depends(get_db),
) -> Any:
    """Get all alerts with optional filtering"""
    query = db.query(Alert)
    
    if severity:
        query = query.filter(Alert.severity == severity)
    if status:
        query = query.filter(Alert.status == status)
    
    alerts = query.offset(skip).limit(limit).all()
    return alerts


@router.post("/", response_model=AlertResponse, status_code=status.HTTP_201_CREATED)
async def create_alert(
    alert_in: AlertCreate,
    current_user: User = Depends(get_current_user),
    db = Depends(get_db),
) -> Any:
    """Create a new alert"""
    alert = Alert(
        **alert_in.dict(),
        created_by_id=current_user.id,
    )
    
    db.add(alert)
    db.commit()
    db.refresh(alert)
    
    # Record metrics
    record_alert(alert.severity, alert.alert_type)
    
    return alert


@router.get("/{alert_id}", response_model=AlertResponse)
async def get_alert(
    alert_id: int,
    current_user: User = Depends(get_current_user),
    db = Depends(get_db),
) -> Any:
    """Get a specific alert by ID"""
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found",
        )
    
    return alert


@router.put("/{alert_id}", response_model=AlertResponse)
async def update_alert(
    alert_id: int,
    alert_in: AlertUpdate,
    current_user: User = Depends(get_current_user),
    db = Depends(get_db),
) -> Any:
    """Update an alert"""
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found",
        )
    
    # Check if status is changing to resolved
    was_resolved = False
    if alert_in.status == "resolved" and alert.status != "resolved":
        was_resolved = True
    
    # Update alert attributes
    for field, value in alert_in.dict(exclude_unset=True).items():
        setattr(alert, field, value)
    
    alert.updated_by_id = current_user.id
    
    db.commit()
    db.refresh(alert)
    
    # Update metrics if alert was resolved
    if was_resolved:
        resolve_alert(alert.severity)
    
    return alert


@router.delete("/{alert_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_alert(
    alert_id: int,
    current_user: User = Depends(get_current_user),
    db = Depends(get_db),
) -> None:
    """Delete an alert"""
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found",
        )
    
    db.delete(alert)
    db.commit()