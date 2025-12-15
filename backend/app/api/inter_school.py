from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from pydantic import BaseModel
from typing import Optional
import os
import uuid
from datetime import datetime
from ..core.database import get_db
from ..models.user import User, UserRole
from ..models.connection_request import ConnectionRequest, ConnectionStatus
from ..models.inter_school_message import InterSchoolMessage
from ..core.security import get_current_user

router = APIRouter(prefix="/inter-school", tags=["inter-school"])

class ConnectionRequestModel(BaseModel):
    receiver_id: int
    message: Optional[str] = None

@router.get("/all-users")
def get_all_users(
    search: str = "",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all system users grouped by schools"""
    from ..models.school import School
    
    # Get all schools
    schools = db.query(School).order_by(School.name).all()
    
    result = []
    for school in schools:
        # Get users from this school (exclude current user)
        query = db.query(User).filter(
            User.school_id == school.id,
            User.id != current_user.id,
            User.role.in_([UserRole.STUDENT, UserRole.TEACHER, UserRole.ADMIN])
        )
        
        if search:
            query = query.filter(
                or_(
                    User.full_name.ilike(f"%{search}%"),
                    User.email.ilike(f"%{search}%")
                )
            )
        
        users = query.order_by(User.full_name).all()
        
        if users:
            school_data = {
                "school_id": school.id,
                "school_name": school.name,
                "province": school.province,
                "district": school.district,
                "users": []
            }
            
            for user in users:
                # Check if already connected
                connection = db.query(ConnectionRequest).filter(
                    or_(
                        and_(ConnectionRequest.sender_id == current_user.id, ConnectionRequest.receiver_id == user.id),
                        and_(ConnectionRequest.sender_id == user.id, ConnectionRequest.receiver_id == current_user.id)
                    ),
                    ConnectionRequest.status == ConnectionStatus.ACCEPTED
                ).first()
                
                school_data["users"].append({
                    "id": user.id,
                    "full_name": user.full_name,
                    "email": user.email,
                    "role": user.role.value,
                    "selected_trade": user.selected_trade,
                    "selected_level": user.selected_level,
                    "connection_id": connection.id if connection else None
                })
            
            result.append(school_data)
    
    return {"schools": result, "total_schools": len(result)}

@router.post("/request/{user_id}")
def send_connection_request(
    user_id: int,
    message: str = "",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send connection request with role-based rules"""
    receiver = db.query(User).filter(User.id == user_id).first()
    if not receiver:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Role-based validation
    sender_role = current_user.role.value.upper()
    receiver_role = receiver.role.value.upper()
    
    # Student can request: Student or Teacher
    if sender_role == "STUDENT" and receiver_role not in ["STUDENT", "TEACHER"]:
        raise HTTPException(status_code=403, detail="Students can only connect with students or teachers")
    
    # Teacher can request: Teacher or DOS/Admin
    if sender_role == "TEACHER" and receiver_role not in ["TEACHER", "ADMIN"]:
        raise HTTPException(status_code=403, detail="Teachers can only connect with teachers or DOS")
    
    # DOS can request: Only DOS
    if sender_role == "ADMIN" and receiver_role != "ADMIN":
        raise HTTPException(status_code=403, detail="DOS can only connect with other DOS")
    
    # Check if request already exists
    existing = db.query(ConnectionRequest).filter(
        or_(
            and_(ConnectionRequest.sender_id == current_user.id, ConnectionRequest.receiver_id == user_id),
            and_(ConnectionRequest.sender_id == user_id, ConnectionRequest.receiver_id == current_user.id)
        )
    ).first()
    
    if existing:
        if existing.status == ConnectionStatus.PENDING:
            raise HTTPException(status_code=400, detail="Request already pending")
        elif existing.status == ConnectionStatus.ACCEPTED:
            raise HTTPException(status_code=400, detail="Already connected")
        elif existing.status == ConnectionStatus.REJECTED:
            # Allow re-request after rejection
            existing.status = ConnectionStatus.PENDING
            existing.message = message
            existing.sender_id = current_user.id
            existing.receiver_id = user_id
            db.commit()
            return {"success": True, "message": "Request sent again"}
    
    # Create new request
    connection = ConnectionRequest(
        sender_id=current_user.id,
        receiver_id=user_id,
        message=message,
        status=ConnectionStatus.PENDING
    )
    
    db.add(connection)
    db.commit()
    db.refresh(connection)
    
    return {"success": True, "message": "Connection request sent"}

@router.get("/pending-requests")
def get_pending_requests(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get pending connection requests for current user"""
    requests = db.query(ConnectionRequest).filter(
        ConnectionRequest.receiver_id == current_user.id,
        ConnectionRequest.status == ConnectionStatus.PENDING
    ).all()
    
    result = []
    for req in requests:
        sender = db.query(User).filter(User.id == req.sender_id).first()
        from ..models.school import School
        school = db.query(School).filter(School.id == sender.school_id).first()
        
        result.append({
            "id": req.id,
            "sender_id": sender.id,
            "sender_name": sender.full_name,
            "sender_email": sender.email,
            "sender_role": sender.role.value,
            "sender_school": school.name if school else "Unknown",
            "sender_province": sender.province,
            "sender_district": sender.district,
            "sender_trade": sender.selected_trade,
            "sender_level": sender.selected_level,
            "message": req.message,
            "created_at": req.created_at.isoformat() if req.created_at else None
        })
    
    return {"requests": result, "count": len(result)}

@router.post("/accept/{request_id}")
def accept_request(
    request_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Accept connection request"""
    request = db.query(ConnectionRequest).filter(
        ConnectionRequest.id == request_id,
        ConnectionRequest.receiver_id == current_user.id,
        ConnectionRequest.status == ConnectionStatus.PENDING
    ).first()
    
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    
    request.status = ConnectionStatus.ACCEPTED
    db.commit()
    
    return {"success": True, "message": "Connection accepted", "connection_id": request.id}

@router.post("/reject/{request_id}")
def reject_request(
    request_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Reject connection request"""
    request = db.query(ConnectionRequest).filter(
        ConnectionRequest.id == request_id,
        ConnectionRequest.receiver_id == current_user.id,
        ConnectionRequest.status == ConnectionStatus.PENDING
    ).first()
    
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    
    request.status = ConnectionStatus.REJECTED
    db.commit()
    
    return {"success": True, "message": "Request rejected"}



@router.get("/connections")
def get_connections(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all accepted connections"""
    connections = db.query(ConnectionRequest).filter(
        or_(
            ConnectionRequest.sender_id == current_user.id,
            ConnectionRequest.receiver_id == current_user.id
        ),
        ConnectionRequest.status == ConnectionStatus.ACCEPTED
    ).all()
    
    result = []
    for conn in connections:
        other_user_id = conn.receiver_id if conn.sender_id == current_user.id else conn.sender_id
        other_user = db.query(User).filter(User.id == other_user_id).first()
        
        from ..models.school import School
        school = db.query(School).filter(School.id == other_user.school_id).first()
        
        # Get unread count
        unread = db.query(InterSchoolMessage).filter(
            InterSchoolMessage.connection_id == conn.id,
            InterSchoolMessage.receiver_id == current_user.id,
            InterSchoolMessage.is_read == False
        ).count()
        
        # Get last message
        last_msg = db.query(InterSchoolMessage).filter(
            InterSchoolMessage.connection_id == conn.id
        ).order_by(InterSchoolMessage.created_at.desc()).first()
        
        result.append({
            "connection_id": conn.id,
            "user_id": other_user.id,
            "user_name": other_user.full_name,
            "user_email": other_user.email,
            "user_role": other_user.role.value,
            "school_name": school.name if school else "Unknown",
            "province": other_user.province,
            "district": other_user.district,
            "unread_count": unread,
            "last_message": last_msg.content if last_msg else None,
            "last_message_time": last_msg.created_at.isoformat() if last_msg else None
        })
    
    return {"connections": result, "count": len(result)}

@router.get("/messages/{connection_id}")
def get_messages(
    connection_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get messages for a connection"""
    connection = db.query(ConnectionRequest).filter(
        ConnectionRequest.id == connection_id,
        or_(
            ConnectionRequest.sender_id == current_user.id,
            ConnectionRequest.receiver_id == current_user.id
        ),
        ConnectionRequest.status == ConnectionStatus.ACCEPTED
    ).first()
    
    if not connection:
        raise HTTPException(status_code=404, detail="Connection not found")
    
    messages = db.query(InterSchoolMessage).filter(
        InterSchoolMessage.connection_id == connection_id
    ).order_by(InterSchoolMessage.created_at).all()
    
    # Mark as read
    db.query(InterSchoolMessage).filter(
        InterSchoolMessage.connection_id == connection_id,
        InterSchoolMessage.receiver_id == current_user.id,
        InterSchoolMessage.is_read == False
    ).update({"is_read": True})
    db.commit()
    
    from ..models.message_reaction import MessageReaction
    
    result = []
    for msg in messages:
        sender = db.query(User).filter(User.id == msg.sender_id).first()
        
        # Get reactions for this message
        reactions = db.query(MessageReaction).filter(MessageReaction.message_id == msg.id).all()
        counts = {'👍': 0, '❤️': 0, '😂': 0, '🔥': 0, '🎉': 0}
        user_reactions = {}
        
        for r in reactions:
            if r.emoji in counts:
                counts[r.emoji] += 1
            if r.user_id not in user_reactions:
                user_reactions[r.user_id] = []
            user_reactions[r.user_id].append(r.emoji)
        
        result.append({
            "id": msg.id,
            "sender_id": msg.sender_id,
            "sender_name": sender.full_name if sender else "Unknown",
            "content": msg.content,
            "file_url": msg.file_url,
            "file_name": msg.file_name,
            "file_type": msg.file_type,
            "file_size": msg.file_size,
            "is_mine": msg.sender_id == current_user.id,
            "likes": counts['👍'],
            "loves": counts['❤️'],
            "laughs": counts['😂'],
            "fires": counts['🔥'],
            "parties": counts['🎉'],
            "userReactions": user_reactions,
            "created_at": msg.created_at.isoformat() if msg.created_at else None
        })
    
    return {"messages": result, "count": len(result)}

@router.post("/messages/{connection_id}")
async def send_message(
    connection_id: int,
    content: str = Form(None),
    file: UploadFile = File(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send message to connected user"""
    connection = db.query(ConnectionRequest).filter(
        ConnectionRequest.id == connection_id,
        or_(
            ConnectionRequest.sender_id == current_user.id,
            ConnectionRequest.receiver_id == current_user.id
        ),
        ConnectionRequest.status == ConnectionStatus.ACCEPTED
    ).first()
    
    if not connection:
        raise HTTPException(status_code=404, detail="Connection not found")
    
    receiver_id = connection.receiver_id if connection.sender_id == current_user.id else connection.sender_id
    
    # Handle file upload
    file_url = None
    file_name = None
    file_type = None
    file_size = None
    
    if file:
        upload_dir = "uploads/inter_school"
        os.makedirs(upload_dir, exist_ok=True)
        
        file_ext = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_ext}"
        file_path = os.path.join(upload_dir, unique_filename)
        
        with open(file_path, "wb") as f:
            f.write(await file.read())
        
        file_url = f"/uploads/inter_school/{unique_filename}"
        file_name = file.filename
        file_type = file.content_type
        file_size = os.path.getsize(file_path)
    
    message = InterSchoolMessage(
        connection_id=connection_id,
        sender_id=current_user.id,
        receiver_id=receiver_id,
        content=content,
        file_url=file_url,
        file_name=file_name,
        file_type=file_type,
        file_size=file_size
    )
    
    db.add(message)
    db.commit()
    db.refresh(message)
    
    return {"success": True, "message_id": message.id}

@router.post("/messages/{message_id}/react")
def toggle_reaction(
    message_id: int,
    emoji: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Toggle reaction on a message"""
    from ..models.message_reaction import MessageReaction
    
    # Check if message exists and user has access
    message = db.query(InterSchoolMessage).filter(InterSchoolMessage.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    # Check if user already reacted with this emoji
    existing = db.query(MessageReaction).filter(
        MessageReaction.message_id == message_id,
        MessageReaction.user_id == current_user.id,
        MessageReaction.emoji == emoji
    ).first()
    
    if existing:
        # Remove reaction
        db.delete(existing)
        db.commit()
        action = "removed"
    else:
        # Add reaction
        reaction = MessageReaction(
            message_id=message_id,
            user_id=current_user.id,
            emoji=emoji
        )
        db.add(reaction)
        db.commit()
        action = "added"
    
    # Get updated counts
    reactions = db.query(MessageReaction).filter(MessageReaction.message_id == message_id).all()
    counts = {}
    user_reactions = {}
    
    for r in reactions:
        counts[r.emoji] = counts.get(r.emoji, 0) + 1
        if r.user_id not in user_reactions:
            user_reactions[r.user_id] = []
        user_reactions[r.user_id].append(r.emoji)
    
    return {
        "success": True,
        "action": action,
        "counts": counts,
        "user_reactions": user_reactions
    }

@router.get("/messages/{message_id}/reactions")
def get_reactions(
    message_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all reactions for a message"""
    from ..models.message_reaction import MessageReaction
    
    reactions = db.query(MessageReaction).filter(MessageReaction.message_id == message_id).all()
    
    counts = {}
    user_reactions = {}
    
    for r in reactions:
        counts[r.emoji] = counts.get(r.emoji, 0) + 1
        if r.user_id not in user_reactions:
            user_reactions[r.user_id] = []
        user_reactions[r.user_id].append(r.emoji)
    
    return {
        "counts": counts,
        "user_reactions": user_reactions
    }

@router.delete("/connections/{connection_id}")
def disconnect(
    connection_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Disconnect from user"""
    connection = db.query(ConnectionRequest).filter(
        ConnectionRequest.id == connection_id,
        or_(
            ConnectionRequest.sender_id == current_user.id,
            ConnectionRequest.receiver_id == current_user.id
        )
    ).first()
    
    if not connection:
        raise HTTPException(status_code=404, detail="Connection not found")
    
    connection.status = ConnectionStatus.BLOCKED
    db.commit()
    
    return {"success": True, "message": "Disconnected"}
