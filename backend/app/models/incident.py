from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from ..core.database import Base
import enum

class IncidentSeverity(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class IncidentStatus(str, enum.Enum):
    PENDING = "pending"
    REVIEWED = "reviewed"
    RESOLVED = "resolved"
    DISMISSED = "dismissed"

class Incident(Base):
    __tablename__ = "incidents"
    
    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(Integer, ForeignKey("messages.id"), nullable=False, index=True)
    reporter_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    reason = Column(Text, nullable=False)
    severity = Column(Enum(IncidentSeverity), default=IncidentSeverity.LOW)
    status = Column(Enum(IncidentStatus), default=IncidentStatus.PENDING)
    decision = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    reviewed_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Relationships
    message = relationship("Message", back_populates="incidents")
    reporter = relationship("User", foreign_keys=[reporter_id], back_populates="incidents_reported")
