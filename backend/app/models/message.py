from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey, DateTime, func, JSON
from sqlalchemy.orm import relationship
from ..core.database import Base
import enum

class MessageStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    HIDDEN = "hidden"

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    channel_id = Column(Integer, ForeignKey("channels.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    content = Column(Text, nullable=True)
    status = Column(Enum(MessageStatus), default=MessageStatus.APPROVED)
    attachments = Column(JSON, default=[])  # [{url, type, size}]
    reply_to_id = Column(Integer, ForeignKey("messages.id"), nullable=True, index=True)
    file_url = Column(String, nullable=True)
    file_name = Column(String, nullable=True)
    file_type = Column(String, nullable=True)
    file_size = Column(Integer, nullable=True)
    format_data = Column(JSON, nullable=True)  # Store text formatting
    scheduled_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    approved_at = Column(DateTime(timezone=True), nullable=True)
    approved_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Relationships
    channel = relationship("Channel", back_populates="messages")
    user = relationship("User", back_populates="messages", foreign_keys=[user_id])
    incidents = relationship("Incident", back_populates="message")
