from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from ..models.message import MessageStatus

class MessageCreate(BaseModel):
    channel_id: int
    content: str
    attachments: List[dict] = []
    scheduled_at: Optional[datetime] = None

class MessageResponse(BaseModel):
    id: int
    channel_id: int
    user_id: int
    content: str
    status: MessageStatus
    attachments: List[dict]
    created_at: datetime
    
    class Config:
        from_attributes = True

class MessageApprove(BaseModel):
    message_id: int
    approved: bool
