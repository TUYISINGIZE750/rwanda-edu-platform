from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, JSON
from sqlalchemy.orm import relationship
from ..core.database import Base

class Pack(Base):
    __tablename__ = "packs"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    resource_ids = Column(JSON, default=[])  # List of resource IDs
    audience_group_id = Column(Integer, ForeignKey("groups.id"), nullable=False, index=True)
    version = Column(Integer, default=1)
    checksum = Column(String, nullable=True)
    size = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    audience_group = relationship("Group", back_populates="packs")
