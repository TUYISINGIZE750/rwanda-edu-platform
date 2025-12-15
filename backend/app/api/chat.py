"""Chat API for group messaging"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from ..core.database import get_db
from ..models.user import User, UserRole
from ..models.channel import Channel
from ..models.message import Message, MessageStatus
from ..core.security import get_current_user

router = APIRouter(prefix="/chat", tags=["chat"])

@router.get("/test")
def test_chat():
    """Test endpoint to verify chat API is working"""
    return {"status": "ok", "message": "Chat API is working", "auto_approve": True}

class SendMessageRequest(BaseModel):
    content: str
    type: Optional[str] = "text"
    attachments: Optional[list] = []

@router.get("/channels/{channel_id}/messages")
def get_channel_messages(
    channel_id: int,
    page: int = 1,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get messages from a channel"""
    channel = db.query(Channel).filter(Channel.id == channel_id).first()
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")
    
    offset = (page - 1) * limit
    
    messages = db.query(Message).filter(
        Message.channel_id == channel_id,
        Message.status == MessageStatus.APPROVED
    ).order_by(desc(Message.created_at)).offset(offset).limit(limit).all()
    
    result = []
    for msg in messages:
        sender = db.query(User).filter(User.id == msg.user_id).first()
        result.append({
            "id": msg.id,
            "content": msg.content,
            "sender": {
                "id": sender.id if sender else 0,
                "name": sender.full_name if sender else "Unknown",
                "role": sender.role.value if sender else "student"
            },
            "sender_id": msg.user_id,
            "status": msg.status.value,
            "timestamp": msg.created_at.isoformat() if msg.created_at else None,
            "created_at": msg.created_at.isoformat() if msg.created_at else None
        })
    
    # Return in chronological order (oldest first)
    return result[::-1]

@router.post("/channels/{channel_id}/messages")
def send_message(
    channel_id: int,
    request: SendMessageRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send a message to a channel"""
    channel = db.query(Channel).filter(Channel.id == channel_id).first()
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")
    
    # Smart approval logic:
    # 1. Teacher messages → Always approved
    # 2. Student → Student in DISCUSSION/RESOURCES → Approved
    # 3. Student → Teacher (ANNOUNCEMENTS) → Needs approval
    # 4. Teacher → Teacher → Always approved
    
    if current_user.role == UserRole.TEACHER:
        # Teachers always approved
        status = MessageStatus.APPROVED
    elif channel.type.value == 'ANNOUNCEMENTS':
        # Students in announcements need approval
        status = MessageStatus.PENDING
    else:
        # Students in discussion/resources auto-approved
        status = MessageStatus.APPROVED
    
    message = Message(
        channel_id=channel_id,
        user_id=current_user.id,
        content=request.content,
        status=status
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    
    return {
        "id": message.id,
        "content": message.content,
        "sender": {
            "id": current_user.id,
            "name": current_user.full_name,
            "role": current_user.role.value
        },
        "sender_id": current_user.id,
        "status": message.status.value,
        "timestamp": message.created_at.isoformat() if message.created_at else None,
        "created_at": message.created_at.isoformat() if message.created_at else None,
        "message": "Message sent successfully"
    }
