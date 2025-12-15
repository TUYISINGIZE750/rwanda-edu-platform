from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime, func, Text
from sqlalchemy.orm import relationship
from ..core.database import Base
import enum

class ConnectionStatus(str, enum.Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    BLOCKED = "BLOCKED"

class ConnectionRequest(Base):
    __tablename__ = "connection_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    receiver_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    status = Column(Enum(ConnectionStatus), default=ConnectionStatus.PENDING)
    message = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    sender = relationship("User", foreign_keys=[sender_id])
    receiver = relationship("User", foreign_keys=[receiver_id])
