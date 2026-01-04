from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from ..core.database import Base
from datetime import datetime
import enum

class NotificationType(str, enum.Enum):
    RESOURCE_UPLOADED = "RESOURCE_UPLOADED"
    NEW_ANNOUNCEMENT = "NEW_ANNOUNCEMENT"
    NEW_MESSAGE = "NEW_MESSAGE"
    CLASS_ASSIGNED = "CLASS_ASSIGNED"
    GROUP_ASSIGNED = "GROUP_ASSIGNED"
    DM_REQUEST = "DM_REQUEST"
    MESSAGE_APPROVED = "MESSAGE_APPROVED"
    MESSAGE_REJECTED = "MESSAGE_REJECTED"
    TEACHER_ASSIGNED = "TEACHER_ASSIGNED"

class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    type = Column(Enum(NotificationType), nullable=False)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    link = Column(String(500), nullable=True)  # URL to navigate to
    is_read = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Optional: Reference to related entity
    related_id = Column(Integer, nullable=True)  # ID of resource, message, etc.
    related_type = Column(String(50), nullable=True)  # "resource", "message", "group", etc.
    
    # Relationship
    user = relationship("User", foreign_keys=[user_id])
    
    def __repr__(self):
        return f"<Notification {self.id} - {self.type} for User {self.user_id}>"
