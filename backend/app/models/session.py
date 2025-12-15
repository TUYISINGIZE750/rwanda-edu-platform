from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, func, JSON
from sqlalchemy.orm import relationship
from ..core.database import Base

class Session(Base):
    __tablename__ = "sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    channel_id = Column(Integer, ForeignKey("channels.id"), nullable=False, index=True)
    jitsi_link = Column(String, nullable=False)
    title = Column(String, nullable=False)
    scheduled_at = Column(DateTime(timezone=True), nullable=False)
    consent_required = Column(Boolean, default=True)
    audio_first = Column(Boolean, default=True)
    attendance = Column(JSON, default=[])  # [{user_id, joined_at, left_at}]
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    channel = relationship("Channel", back_populates="sessions")
