from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime, Boolean, func
from sqlalchemy.orm import relationship
from ..core.database import Base
import enum

class LiveSessionType(str, enum.Enum):
    AUDIO = "AUDIO"
    VIDEO = "VIDEO"

class LiveSessionStatus(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    ACTIVE = "ACTIVE"
    ENDED = "ENDED"
    REJECTED = "REJECTED"

class LiveSession(Base):
    __tablename__ = "live_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    channel_id = Column(Integer, ForeignKey("channels.id"), nullable=False, index=True)
    host_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    type = Column(Enum(LiveSessionType), nullable=False)
    status = Column(Enum(LiveSessionStatus), default=LiveSessionStatus.PENDING)
    title = Column(String, nullable=False)
    room_id = Column(String, unique=True, index=True)
    started_at = Column(DateTime(timezone=True))
    ended_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    host = relationship("User", foreign_keys=[host_id])
    channel = relationship("Channel")
