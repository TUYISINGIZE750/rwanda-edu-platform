from pydantic import BaseModel
from datetime import datetime
from ..models.incident import IncidentSeverity, IncidentStatus

class IncidentCreate(BaseModel):
    message_id: int
    reason: str
    severity: IncidentSeverity = IncidentSeverity.LOW

class IncidentResponse(BaseModel):
    id: int
    message_id: int
    reporter_id: int
    reason: str
    severity: IncidentSeverity
    status: IncidentStatus
    created_at: datetime
    
    class Config:
        from_attributes = True
