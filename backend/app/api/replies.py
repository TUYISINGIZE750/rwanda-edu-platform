from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel
from ..core.database import get_db
from ..models.message import Message
from ..models.user import User

router = APIRouter(prefix="/replies", tags=["replies"])

class ReplyCreate(BaseModel):
    message_id: int
    reply_to_id: int
    content: str
    attachments: Optional[list] = []

@router.post("/")
async def create_reply(reply: ReplyCreate, db: Session = Depends(get_db)):
    """Create a reply to a message"""
    original_msg = db.query(Message).filter(Message.id == reply.reply_to_id).first()
    if not original_msg:
        raise HTTPException(status_code=404, detail="Original message not found")
    
    message = db.query(Message).filter(Message.id == reply.message_id).first()
    if message:
        message.reply_to_id = reply.reply_to_id
        db.commit()
        return {"success": True, "message": "Reply linked successfully"}
    
    raise HTTPException(status_code=404, detail="Message not found")

@router.get("/message/{message_id}")
async def get_message_replies(message_id: int, db: Session = Depends(get_db)):
    """Get all replies to a specific message"""
    replies = db.query(Message).filter(Message.reply_to_id == message_id).all()
    
    result = []
    for reply in replies:
        user = db.query(User).filter(User.id == reply.user_id).first()
        result.append({
            "id": reply.id,
            "content": reply.content,
            "sender_name": user.full_name if user else "Unknown",
            "sender_role": user.role.value if user else "student",
            "created_at": reply.created_at.isoformat() if reply.created_at else None,
            "attachments": reply.attachments or []
        })
    
    return {"replies": result, "count": len(result)}
