from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.core.security import get_current_user
from app.models.user import User
from app.models.incident import Incident
from app.schemas.incident import IncidentCreate, IncidentResponse, IncidentUpdate
from app.core.metrics import record_incident, resolve_incident
from app.db.session import get_db

router = APIRouter()


@router.get("/", response_model=List[IncidentResponse])
async def get_incidents(
    severity: Optional[str] = Query(None, description="Filter by severity"),
    status: Optional[str] = Query(None, description="Filter by status"),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db = Depends(get_db),
) -> Any:
    """Get all incidents with optional filtering"""
    query = db.query(Incident)
    
    if severity:
        query = query.filter(Incident.severity == severity)
    if status:
        query = query.filter(Incident.status == status)
    
    incidents = query.offset(skip).limit(limit).all()
    return incidents


@router.post("/", response_model=IncidentResponse, status_code=status.HTTP_201_CREATED)
async def create_incident(
    incident_in: IncidentCreate,
    current_user: User = Depends(get_current_user),
    db = Depends(get_db),
) -> Any:
    """Create a new incident"""
    incident = Incident(
        **incident_in.dict(),
        created_by_id=current_user.id,
    )
    
    db.add(incident)
    db.commit()
    db.refresh(incident)
    
    # Record metrics
    record_incident(incident.severity, incident.status)
    
    return incident


@router.get("/{incident_id}", response_model=IncidentResponse)
async def get_incident(
    incident_id: int,
    current_user: User = Depends(get_current_user),
    db = Depends(get_db),
) -> Any:
    """Get a specific incident by ID"""
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incident not found",
        )
    
    return incident


@router.put("/{incident_id}", response_model=IncidentResponse)
async def update_incident(
    incident_id: int,
    incident_in: IncidentUpdate,
    current_user: User = Depends(get_current_user),
    db = Depends(get_db),
) -> Any:
    """Update an incident"""
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incident not found",
        )
    
    # Check if status is changing to resolved
    was_resolved = False
    if incident_in.status == "resolved" and incident.status != "resolved":
        was_resolved = True
    
    # Update incident attributes
    for field, value in incident_in.dict(exclude_unset=True).items():
        setattr(incident, field, value)
    
    incident.updated_by_id = current_user.id
    
    db.commit()
    db.refresh(incident)
    
    # Update metrics if incident was resolved
    if was_resolved:
        resolve_incident(incident.severity)
    
    return incident


@router.delete("/{incident_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_incident(
    incident_id: int,
    current_user: User = Depends(get_current_user),
    db = Depends(get_db),
) -> None:
    """Delete an incident"""
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incident not found",
        )
    
    db.delete(incident)
    db.commit()