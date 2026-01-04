from sqlalchemy import Column, Integer, String, ARRAY
from ..core.database import Base

class School(Base):
    __tablename__ = "schools"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    type = Column(String, nullable=False)
    category = Column(String, nullable=False)
    province = Column(String, nullable=False, index=True)
    district = Column(String, nullable=False, index=True)
    trades = Column(ARRAY(String), nullable=True)
    
    def __repr__(self):
        return f"<School {self.name} - {self.district}>"
