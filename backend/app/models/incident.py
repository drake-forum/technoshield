from sqlalchemy import Column, String, Integer, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class Incident(BaseModel):
    """Incident model for security incidents"""
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=False)
    severity = Column(String(50), nullable=False, index=True)  # critical, high, medium, low
    status = Column(String(50), nullable=False, index=True, default="open")  # open, investigating, contained, resolved
    
    # Incident details
    incident_type = Column(String(100), nullable=False, index=True)  # data breach, ransomware, ddos, etc.
    affected_systems = Column(Text, nullable=True)  # List of affected systems/assets
    impact_assessment = Column(Text, nullable=True)  # Assessment of business impact
    
    # Timeline tracking
    detected_at = Column(DateTime, nullable=True)
    contained_at = Column(DateTime, nullable=True)
    resolved_at = Column(DateTime, nullable=True)
    
    # Resolution and response
    response_strategy = Column(Text, nullable=True)  # Containment and eradication strategy
    resolution_summary = Column(Text, nullable=True)  # Summary of resolution actions
    lessons_learned = Column(Text, nullable=True)  # Post-incident analysis
    
    # User relationships
    created_by_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    created_by = relationship("User", foreign_keys=[created_by_id])
    
    updated_by_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    updated_by = relationship("User", foreign_keys=[updated_by_id])
    
    assigned_to_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    assigned_to = relationship("User", foreign_keys=[assigned_to_id])
    
    # Related alerts
    alerts = relationship("Alert", back_populates="incident")