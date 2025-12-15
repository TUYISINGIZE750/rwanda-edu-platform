"""Direct Messages API"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, desc
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from ..core.database import get_db
from ..models.user import User, UserRole
from ..models.direct_message import DirectMessage, DMStatus
from ..core.security import get_current_user

router = APIRouter(prefix="/dm", tags=["direct-messages"])

class SendDMRequest(BaseModel):
    receiver_id: int
    content: str

@router.get("/conversations")
def get_conversations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get list of conversations for current user"""
    # Get unique users the current user has messaged with
    sent_to = db.query(DirectMessage.receiver_id).filter(
        DirectMessage.sender_id == current_user.id
    ).distinct().all()
    
    received_from = db.query(DirectMessage.sender_id).filter(
        DirectMessage.receiver_id == current_user.id
    ).distinct().all()
    
    user_ids = set([u[0] for u in sent_to] + [u[0] for u in received_from])
    
    conversations = []
    for user_id in user_ids:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            continue
            
        # Get last message
        last_msg = db.query(DirectMessage).filter(
            or_(
                and_(DirectMessage.sender_id == current_user.id, DirectMessage.receiver_id == user_id),
                and_(DirectMessage.sender_id == user_id, DirectMessage.receiver_id == current_user.id)
            )
        ).order_by(desc(DirectMessage.created_at)).first()
        
        # Count unread
        unread = db.query(DirectMessage).filter(
            DirectMessage.sender_id == user_id,
            DirectMessage.receiver_id == current_user.id,
            DirectMessage.read_at == None,
            DirectMessage.status == DMStatus.APPROVED
        ).count()
        
        conversations.append({
            "user_id": user.id,
            "user_name": user.full_name,
            "user_role": user.role.value,
            "last_message": last_msg.content if last_msg else "",
            "last_message_time": last_msg.created_at.isoformat() if last_msg else None,
            "unread_count": unread
        })
    
    return conversations

@router.get("/messages/{user_id}")
def get_messages_with_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all messages between current user and specified user"""
    messages = db.query(DirectMessage).filter(
        or_(
            and_(DirectMessage.sender_id == current_user.id, DirectMessage.receiver_id == user_id),
            and_(DirectMessage.sender_id == user_id, DirectMessage.receiver_id == current_user.id)
        ),
        DirectMessage.status == DMStatus.APPROVED
    ).order_by(DirectMessage.created_at).all()
    
    # Mark received messages as read
    db.query(DirectMessage).filter(
        DirectMessage.sender_id == user_id,
        DirectMessage.receiver_id == current_user.id,
        DirectMessage.read_at == None
    ).update({"read_at": datetime.utcnow()})
    db.commit()
    
    result = []
    for msg in messages:
        sender = db.query(User).filter(User.id == msg.sender_id).first()
        result.append({
            "id": msg.id,
            "content": msg.content,
            "sender_id": msg.sender_id,
            "sender_name": sender.full_name if sender else "Unknown",
            "is_own": msg.sender_id == current_user.id,
            "created_at": msg.created_at.isoformat(),
            "read": msg.read_at is not None
        })
    
    return result

@router.post("/send")
def send_direct_message(
    request: SendDMRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send a direct message"""
    receiver = db.query(User).filter(User.id == request.receiver_id).first()
    if not receiver:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Determine if approval needed
    # Student → Teacher: needs approval
    # Student → Student: auto-approved
    # Teacher → Anyone: auto-approved
    if current_user.role == UserRole.STUDENT and receiver.role == UserRole.TEACHER:
        status = DMStatus.PENDING
    else:
        status = DMStatus.APPROVED
    
    dm = DirectMessage(
        sender_id=current_user.id,
        receiver_id=request.receiver_id,
        content=request.content,
        status=status
    )
    db.add(dm)
    db.commit()
    db.refresh(dm)
    
    return {
        "id": dm.id,
        "content": dm.content,
        "status": dm.status.value,
        "created_at": dm.created_at.isoformat(),
        "message": "Message sent" if status == DMStatus.APPROVED else "Message pending teacher approval"
    }

@router.get("/pending")
def get_pending_messages(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get pending DMs for teachers"""
    if current_user.role != UserRole.TEACHER:
        raise HTTPException(status_code=403, detail="Teachers only")
    
    pending = db.query(DirectMessage).filter(
        DirectMessage.receiver_id == current_user.id,
        DirectMessage.status == DMStatus.PENDING
    ).order_by(desc(DirectMessage.created_at)).all()
    
    result = []
    for msg in pending:
        sender = db.query(User).filter(User.id == msg.sender_id).first()
        result.append({
            "id": msg.id,
            "content": msg.content,
            "sender_id": msg.sender_id,
            "sender_name": sender.full_name if sender else "Unknown",
            "created_at": msg.created_at.isoformat()
        })
    
    return result

@router.post("/approve/{message_id}")
def approve_dm(
    message_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Approve a pending DM"""
    if current_user.role != UserRole.TEACHER:
        raise HTTPException(status_code=403, detail="Teachers only")
    
    msg = db.query(DirectMessage).filter(
        DirectMessage.id == message_id,
        DirectMessage.receiver_id == current_user.id
    ).first()
    
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found")
    
    msg.status = DMStatus.APPROVED
    db.commit()
    
    return {"message": "Message approved"}

@router.post("/reject/{message_id}")
def reject_dm(
    message_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Reject a pending DM"""
    if current_user.role != UserRole.TEACHER:
        raise HTTPException(status_code=403, detail="Teachers only")
    
    msg = db.query(DirectMessage).filter(
        DirectMessage.id == message_id,
        DirectMessage.receiver_id == current_user.id
    ).first()
    
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found")
    
    msg.status = DMStatus.REJECTED
    db.commit()
    
    return {"message": "Message rejected"}
