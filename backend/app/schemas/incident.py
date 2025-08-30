from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, validator

from app.schemas.base import BaseSchema, BaseResponseSchema


class IncidentBase(BaseSchema):
    """Base schema for incident data"""
    title: Optional[str] = None
    description: Optional[str] = None
    severity: Optional[str] = None
    status: Optional[str] = None
    incident_type: Optional[str] = None
    affected_systems: Optional[str] = None
    impact_assessment: Optional[str] = None
    response_strategy: Optional[str] = None
    resolution_summary: Optional[str] = None
    lessons_learned: Optional[str] = None
    assigned_to_id: Optional[int] = None


class IncidentCreate(IncidentBase):
    """Schema for incident creation"""
    title: str
    description: str
    severity: str
    incident_type: str
    
    @validator("severity")
    def validate_severity(cls, v):
        allowed_values = ["critical", "high", "medium", "low"]
        if v not in allowed_values:
            raise ValueError(f"Severity must be one of: {', '.join(allowed_values)}")
        return v


class IncidentUpdate(IncidentBase):
    """Schema for incident update"""
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
            allowed_values = ["open", "investigating", "contained", "resolved"]
            if v not in allowed_values:
                raise ValueError(f"Status must be one of: {', '.join(allowed_values)}")
        return v


class IncidentResponse(BaseResponseSchema):
    """Schema for incident response"""
    title: str
    description: str
    severity: str
    status: str
    incident_type: str
    affected_systems: Optional[str] = None
    impact_assessment: Optional[str] = None
    detected_at: Optional[datetime] = None
    contained_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    response_strategy: Optional[str] = None
    resolution_summary: Optional[str] = None
    lessons_learned: Optional[str] = None
    created_by_id: Optional[int] = None
    updated_by_id: Optional[int] = None
    assigned_to_id: Optional[int] = None