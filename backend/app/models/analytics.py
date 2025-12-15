from sqlalchemy import Column, Integer, String, Float, DateTime, func
from ..core.database import Base

class Analytics(Base):
    __tablename__ = "analytics"
    
    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, nullable=False, index=True)
    class_id = Column(Integer, nullable=True, index=True)
    metric_type = Column(String, nullable=False)  # engagement, messages, resources, attendance
    metric_value = Column(Float, nullable=False)
    period = Column(String, nullable=False)  # daily, weekly, monthly
    recorded_at = Column(DateTime(timezone=True), server_default=func.now())
