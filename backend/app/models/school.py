from sqlalchemy import Column, Integer, String, Text
from ..core.database import Base
import json

class School(Base):
    __tablename__ = "schools"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    type = Column(String, nullable=False)
    category = Column(String, nullable=False)
    province = Column(String, nullable=False, index=True)
    district = Column(String, nullable=False, index=True)
    trades_json = Column(String, nullable=True)
    trades_text = Column('trades', Text, nullable=True)
    
    @property
    def trades(self):
        # Prioritize trades_text column (comma-separated)
        if self.trades_text:
            trades_list = [t.strip() for t in self.trades_text.split(',') if t.strip()]
            return trades_list
        # Fallback to trades_json
        if self.trades_json:
            try:
                return json.loads(self.trades_json)
            except:
                return []
        return []
    
    @trades.setter
    def trades(self, value):
        if value:
            if isinstance(value, list):
                self.trades_text = ','.join(value)
                self.trades_json = json.dumps(value)
            elif isinstance(value, str):
                self.trades_text = value
        else:
            self.trades_text = None
            self.trades_json = None
    
    def __repr__(self):
        return f"<School {self.name} - {self.district}>"
