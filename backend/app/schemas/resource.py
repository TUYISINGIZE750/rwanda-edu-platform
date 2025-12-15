from pydantic import BaseModel
from datetime import datetime

class ResourceCreate(BaseModel):
    title: str
    type: str
    url: str
    size: int = 0
    metadata: dict = {}

class ResourceResponse(BaseModel):
    id: int
    owner_id: int
    title: str
    type: str
    url: str
    size: int
    created_at: datetime
    
    class Config:
        from_attributes = True
