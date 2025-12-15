from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from ..core.database import Base
import enum

class ChannelType(str, enum.Enum):
    ANNOUNCEMENTS = "ANNOUNCEMENTS"
    DISCUSSION = "DISCUSSION"
    OFFICE_HOURS = "OFFICE_HOURS"
    RESOURCES = "RESOURCES"

class Channel(Base):
    __tablename__ = "channels"
    
    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False, index=True)
    name = Column(String, nullable=False)
    type = Column(Enum(ChannelType), nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    group = relationship("Group", back_populates="channels")
    messages = relationship("Message", back_populates="channel")
    sessions = relationship("Session", back_populates="channel")
