from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from ..core.database import get_db
from ..models.user import User, UserRole
from ..models.message import Message, MessageStatus
from ..models.channel import Channel
from ..core.security import get_current_user

router = APIRouter(prefix="/messages", tags=["messages"])

@router.get("/channel/{channel_id}")
def get_channel_messages(
    channel_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify channel exists and user has access
    channel = db.query(Channel).filter(Channel.id == channel_id).first()
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")
    
    # Get messages from database
    messages = db.query(Message, User).join(
        User, Message.user_id == User.id
    ).filter(
        Message.channel_id == channel_id,
        Message.status == MessageStatus.APPROVED
    ).order_by(Message.created_at.asc()).all()
    
    result = []
    for msg, user in messages:
        result.append({
            "id": msg.id,
            "content": msg.content,
            "author_name": user.full_name,
            "created_at": msg.created_at.isoformat(),
            "status": msg.status.value,
            "attachments": msg.attachments or []
        })
    
    return result

@router.post("/")
def send_message(
    message_data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    channel_id = message_data.get("channel_id")
    content = message_data.get("content", "").strip()
    
    if not channel_id or not content:
        raise HTTPException(status_code=400, detail="Channel ID and content required")
    
    # Verify channel exists
    channel = db.query(Channel).filter(Channel.id == channel_id).first()
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")
    
    # Get attachments from request
    attachments = message_data.get("attachments", [])
    
    # Create message
    message = Message(
        content=content,
        channel_id=channel_id,
        user_id=current_user.id,
        status=MessageStatus.APPROVED,
        attachments=attachments,
        created_at=datetime.now()
    )
    
    db.add(message)
    db.commit()
    db.refresh(message)
    
    return {
        "id": message.id,
        "content": message.content,
        "author_name": current_user.full_name,
        "created_at": message.created_at.isoformat(),
        "status": message.status.value,
        "attachments": message.attachments or []
    }