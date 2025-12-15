"""Simple Working Chat API"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from sqlalchemy import desc
from pydantic import BaseModel
from datetime import datetime
import os
import uuid
from ..core.database import get_db
from ..models.user import User, UserRole
from ..models.channel import Channel, ChannelType
from ..models.message import Message, MessageStatus
from ..models.group import Group
from ..core.security import get_current_user

router = APIRouter(prefix="/simple-chat", tags=["simple-chat"])

@router.get("/pending-messages")
def get_pending_messages(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all pending messages for teacher approval"""
    if current_user.role != UserRole.TEACHER:
        raise HTTPException(status_code=403, detail="Teachers only")
    
    # Get all pending messages from channels in teacher's school
    from ..models.group import Group
    
    pending = db.query(Message).join(Channel).join(Group).filter(
        Group.school_id == current_user.school_id,
        Message.status == MessageStatus.PENDING
    ).order_by(desc(Message.created_at)).all()
    
    result = []
    for msg in pending:
        sender = db.query(User).filter(User.id == msg.user_id).first()
        channel = db.query(Channel).filter(Channel.id == msg.channel_id).first()
        result.append({
            "id": msg.id,
            "content": msg.content,
            "sender_name": sender.full_name if sender else "Unknown",
            "channel_name": channel.name if channel else "Unknown",
            "channel_id": msg.channel_id,
            "created_at": msg.created_at.isoformat() if msg.created_at else None
        })
    
    return {"pending": result, "count": len(result)}

@router.post("/approve-message/{message_id}")
def approve_message(
    message_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Approve a pending message"""
    if current_user.role != UserRole.TEACHER:
        raise HTTPException(status_code=403, detail="Teachers only")
    
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    message.status = MessageStatus.APPROVED
    db.commit()
    
    return {"success": True, "message": "Message approved"}

@router.post("/reject-message/{message_id}")
def reject_message(
    message_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Reject a pending message"""
    if current_user.role != UserRole.TEACHER:
        raise HTTPException(status_code=403, detail="Teachers only")
    
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    message.status = MessageStatus.REJECTED
    db.commit()
    
    return {"success": True, "message": "Message rejected"}

class MessageRequest(BaseModel):
    content: str
    attachments: list = []
    reply_to_id: int = None

@router.get("/channels/{channel_id}/messages")
def get_messages(
    channel_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get messages in a channel (teachers see pending, students see approved only)"""
    # Teachers see ALL messages (including pending), students see only approved
    if current_user.role == UserRole.TEACHER:
        messages = db.query(Message).filter(
            Message.channel_id == channel_id
        ).order_by(Message.created_at).all()
    else:
        messages = db.query(Message).filter(
            Message.channel_id == channel_id,
            Message.status == MessageStatus.APPROVED
        ).order_by(Message.created_at).all()
    
    result = []
    for msg in messages:
        sender = db.query(User).filter(User.id == msg.user_id).first()
        reply_to_msg = None
        if msg.reply_to_id:
            original = db.query(Message).filter(Message.id == msg.reply_to_id).first()
            if original:
                original_sender = db.query(User).filter(User.id == original.user_id).first()
                reply_to_msg = {
                    "id": original.id,
                    "content": original.content[:50] + "..." if len(original.content) > 50 else original.content,
                    "sender_name": original_sender.full_name if original_sender else "Unknown"
                }
        
        result.append({
            "id": msg.id,
            "content": msg.content,
            "sender_id": msg.user_id,
            "sender_name": sender.full_name if sender else "Unknown",
            "sender_role": sender.role.value if sender else "student",
            "status": msg.status.value if msg.status else "approved",
            "created_at": msg.created_at.isoformat() if msg.created_at else datetime.now().isoformat(),
            "timestamp": msg.created_at.isoformat() if msg.created_at else datetime.now().isoformat(),
            "is_mine": msg.user_id == current_user.id,
            "attachments": msg.attachments or [],
            "reply_to": reply_to_msg,
            "file_url": msg.file_url,
            "file_name": msg.file_name,
            "file_type": msg.file_type,
            "file_size": msg.file_size,
            "format_data": msg.format_data
        })
    
    return {"messages": result, "count": len(result)}

@router.post("/channels/{channel_id}/messages")
async def send_message(
    channel_id: int,
    content: str = Form(None),
    reply_to_id: int = Form(None),
    format: str = Form(None),
    file: UploadFile = File(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send a message to a channel with optional file"""
    channel = db.query(Channel).filter(Channel.id == channel_id).first()
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")
    
    # Check if teacher has access to this channel
    if current_user.role == UserRole.TEACHER:
        # Only module creator can send messages
        if channel.created_by != current_user.id:
            raise HTTPException(status_code=403, detail="You don't have access to send messages in this module")
    
    # Handle file upload
    file_url = None
    file_name = None
    file_type = None
    file_size = None
    
    if file:
        # Create uploads directory if it doesn't exist
        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)
        
        # Generate unique filename
        file_ext = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_ext}"
        file_path = os.path.join(upload_dir, unique_filename)
        
        # Save file
        with open(file_path, "wb") as f:
            f.write(await file.read())
        
        file_url = f"/uploads/{unique_filename}"
        file_name = file.filename
        file_type = file.content_type
        file_size = os.path.getsize(file_path)
    
    # Approval logic: Students need approval for ANNOUNCEMENTS channel
    if current_user.role == UserRole.TEACHER:
        status = MessageStatus.APPROVED
    elif channel.type == ChannelType.ANNOUNCEMENTS:
        status = MessageStatus.PENDING
    else:
        status = MessageStatus.APPROVED
    
    # Parse formatting data
    import json
    format_data = None
    if format:
        try:
            format_data = {"textFormat": json.loads(format)}
        except:
            pass
    
    message = Message(
        channel_id=channel_id,
        user_id=current_user.id,
        content=content or "",
        status=status,
        reply_to_id=reply_to_id,
        format_data=format_data,
        file_url=file_url,
        file_name=file_name,
        file_type=file_type,
        file_size=file_size,
        created_at=datetime.now()
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    
    return {
        "success": True,
        "message_id": message.id,
        "status": status.value,
        "content": message.content,
        "sender_name": current_user.full_name,
        "timestamp": message.created_at.isoformat(),
        "file_url": file_url,
        "needs_approval": status == MessageStatus.PENDING
    }
