from sqlalchemy import Column, Integer, String, DateTime, func
from ..core.database import Base

class TeacherClassAccess(Base):
    """Tracks which teachers have access to which classes"""
    __tablename__ = "teacher_class_access"
    
    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, nullable=False, index=True)  # Teacher user ID
    group_id = Column(Integer, nullable=False, index=True)  # Class/Group ID
    granted_by = Column(Integer, nullable=False)  # Class teacher who granted access
    module_name = Column(String, nullable=True)  # e.g., "Mathematics", "Physics"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
