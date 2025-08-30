from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, validator

from app.schemas.base import BaseSchema, BaseResponseSchema


class AlertBase(BaseSchema):
    """Base schema for alert data"""
    title: Optional[str] = None
    description: Optional[str] = None
    severity: Optional[str] = None
    status: Optional[str] = None
    source: Optional[str] = None
    source_ip: Optional[str] = None
    destination_ip: Optional[str] = None
    affected_asset: Optional[str] = None
    alert_type: Optional[str] = None
    raw_data: Optional[str] = None
    resolution_notes: Optional[str] = None


class AlertCreate(AlertBase):
    """Schema for alert creation"""
    title: str
    description: str
    severity: str
    source: str
    alert_type: str
    
    @validator("severity")
    def validate_severity(cls, v):
        allowed_values = ["critical", "high", "medium", "low"]
        if v not in allowed_values:
            raise ValueError(f"Severity must be one of: {', '.join(allowed_values)}")
        return v


class AlertUpdate(AlertBase):
    """Schema for alert update"""
    @validator("severity")
    def validate_severity(cls, v):
        if v is not None:
            allowed_values = ["critical", "high", "medium", "low"]
            if v not in allowed_values:
                raise ValueError(f"Severity must be one of: {', '.join(allowed_values)}")
        return v
    
    @validator("status")
    def validate_status(cls, v):
        if v is not None:
            allowed_values = ["open", "acknowledged", "resolved"]
            if v not in allowed_values:
                raise ValueError(f"Status must be one of: {', '.join(allowed_values)}")
        return v


class AlertResponse(BaseResponseSchema):
    """Schema for alert response"""
    title: str
    description: str
    severity: str
    status: str
    source: str
    source_ip: Optional[str] = None
    destination_ip: Optional[str] = None
    affected_asset: Optional[str] = None
    alert_type: str
    raw_data: Optional[str] = None
    resolved_at: Optional[datetime] = None
    resolution_notes: Optional[str] = None
    created_by_id: Optional[int] = None
    updated_by_id: Optional[int] = None
    incident_id: Optional[int] = None