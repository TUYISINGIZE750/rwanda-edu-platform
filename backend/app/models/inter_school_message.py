from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, Text, Boolean
from sqlalchemy.orm import relationship
from ..core.database import Base

class InterSchoolMessage(Base):
    __tablename__ = "inter_school_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    connection_id = Column(Integer, ForeignKey("connection_requests.id"), nullable=False, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=True)
    file_url = Column(String, nullable=True)
    file_name = Column(String, nullable=True)
    file_type = Column(String, nullable=True)
    file_size = Column(Integer, nullable=True)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    sender = relationship("User", foreign_keys=[sender_id])
    receiver = relationship("User", foreign_keys=[receiver_id])
    connection = relationship("ConnectionRequest")
