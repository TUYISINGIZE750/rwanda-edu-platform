from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from ..core.database import Base
import enum

class DMRequestStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"

class DMRequest(Base):
    __tablename__ = "dm_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    topic = Column(String, nullable=False)
    reason = Column(Text, nullable=False)
    status = Column(Enum(DMRequestStatus), default=DMRequestStatus.PENDING)
    window_start = Column(DateTime(timezone=True), nullable=True)
    window_end = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    student = relationship("User", foreign_keys=[student_id], back_populates="dm_requests_sent")
    teacher = relationship("User", foreign_keys=[teacher_id], back_populates="dm_requests_received")
