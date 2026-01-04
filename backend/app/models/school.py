from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.types import JSON
from ..core.database import Base

class School(Base):
    __tablename__ = "schools"
    
    id = Column(Integer, primary_key=True, index=True)
    school_code = Column(String, nullable=True)
    name = Column(String, nullable=False, index=True)
    type = Column(String, nullable=False)
    category = Column(String, nullable=False)
    province = Column(String, nullable=False, index=True)
    district = Column(String, nullable=False, index=True)
    trades = Column(JSON, nullable=True)
    gender = Column(String, nullable=True)
    
    def __repr__(self):
        return f"<School {self.name} - {self.district}>"
