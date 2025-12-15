from sqlalchemy import Column, Integer, String, Enum, DateTime, func
from sqlalchemy.orm import relationship
from ..core.database import Base
import enum

class GroupType(str, enum.Enum):
    CLASS = "CLASS"
    CLUB = "CLUB"
    TEAM = "TEAM"
    SPECIAL = "SPECIAL"

class Group(Base):
    __tablename__ = "groups"
    
    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, nullable=False, index=True)
    name = Column(String, nullable=False)
    type = Column(Enum(GroupType), nullable=False)
    roster_source = Column(String, default="auto")  # auto, manual
    grade = Column(Integer, nullable=True)
    department = Column(String, nullable=True, index=True)  # TVET trade/department
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    channels = relationship("Channel", back_populates="group")
    packs = relationship("Pack", back_populates="audience_group")
