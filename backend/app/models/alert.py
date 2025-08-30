from sqlalchemy import Column, String, Integer, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class Alert(BaseModel):
    """Alert model for security alerts"""
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=False)
    severity = Column(String(50), nullable=False, index=True)  # critical, high, medium, low
    status = Column(String(50), nullable=False, index=True, default="open")  # open, acknowledged, resolved
    source = Column(String(100), nullable=False, index=True)  # IDS, firewall, SIEM, etc.
    
    # IP addresses and assets involved
    source_ip = Column(String(50), nullable=True, index=True)
    destination_ip = Column(String(50), nullable=True, index=True)
    affected_asset = Column(String(255), nullable=True, index=True)
    
    # Alert metadata
    alert_type = Column(String(100), nullable=False, index=True)  # intrusion, malware, anomaly, etc.
    raw_data = Column(Text, nullable=True)  # Raw alert data in JSON format
    
    # Resolution tracking
    resolved_at = Column(DateTime, nullable=True)
    resolution_notes = Column(Text, nullable=True)
    
    # User relationships
    created_by_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    created_by = relationship("User", foreign_keys=[created_by_id])
    
    updated_by_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    updated_by = relationship("User", foreign_keys=[updated_by_id])
    
    # Related incident if escalated
    incident_id = Column(Integer, ForeignKey("incident.id"), nullable=True)
    incident = relationship("Incident", back_populates="alerts")