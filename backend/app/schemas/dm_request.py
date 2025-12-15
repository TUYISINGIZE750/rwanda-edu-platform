from pydantic import BaseModel
from datetime import datetime
from ..models.dm_request import DMRequestStatus

class DMRequestCreate(BaseModel):
    teacher_id: int
    topic: str
    reason: str

class DMRequestResponse(BaseModel):
    id: int
    student_id: int
    teacher_id: int
    topic: str
    reason: str
    status: DMRequestStatus
    window_start: datetime | None
    window_end: datetime | None
    created_at: datetime
    
    class Config:
        from_attributes = True

class DMRequestApprove(BaseModel):
    approved: bool
    window_hours: int = 48
