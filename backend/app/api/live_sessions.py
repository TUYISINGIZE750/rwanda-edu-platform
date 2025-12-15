from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
import uuid
from ..core.database import get_db
from ..models.user import User, UserRole
from ..models.live_session import LiveSession, LiveSessionType, LiveSessionStatus
from ..core.security import get_current_user

router = APIRouter(prefix="/live-sessions", tags=["live-sessions"])

class LiveSessionRequest(BaseModel):
    channel_id: int
    type: str
    title: str

@router.post("/request")
def request_live_session(
    request: LiveSessionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Request to start a live audio/video session"""
    # Check if there's already an active session in this channel
    active = db.query(LiveSession).filter(
        LiveSession.channel_id == request.channel_id,
        LiveSession.status.in_([LiveSessionStatus.ACTIVE, LiveSessionStatus.APPROVED])
    ).first()
    
    if active:
        raise HTTPException(status_code=400, detail="A live session is already active in this channel")
    
    # Only module creator teachers can start sessions without approval
    from ..models.channel import Channel
    channel = db.query(Channel).filter(Channel.id == request.channel_id).first()
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")
    
    # Module creator auto-approves, others need approval
    is_module_creator = current_user.role == UserRole.TEACHER and channel.created_by == current_user.id
    status = LiveSessionStatus.APPROVED if is_module_creator else LiveSessionStatus.PENDING
    
    # Generate simple room ID without special characters to avoid Jitsi auth requirements
    simple_room_id = f"RwandaEdu{uuid.uuid4().hex[:12]}"
    
    session = LiveSession(
        channel_id=request.channel_id,
        host_id=current_user.id,
        type=LiveSessionType(request.type),
        status=status,
        title=request.title,
        room_id=simple_room_id,
        created_at=datetime.now()
    )
    
    db.add(session)
    db.commit()
    db.refresh(session)
    
    return {
        "success": True,
        "session_id": session.id,
        "status": status.value,
        "room_id": session.room_id,
        "needs_approval": status == LiveSessionStatus.PENDING
    }

@router.get("/channel/{channel_id}")
def get_channel_live_sessions(
    channel_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get active live sessions for a channel"""
    # Only return active sessions
    sessions = db.query(LiveSession).filter(
        LiveSession.channel_id == channel_id,
        LiveSession.status == LiveSessionStatus.ACTIVE
    ).order_by(LiveSession.created_at.desc()).all()
    
    result = []
    for s in sessions:
        host = db.query(User).filter(User.id == s.host_id).first()
        result.append({
            "id": s.id,
            "type": s.type.value,
            "status": s.status.value,
            "title": s.title,
            "room_id": s.room_id,
            "host_name": host.full_name if host else "Unknown",
            "host_id": s.host_id,
            "started_at": s.started_at.isoformat() if s.started_at else None,
            "created_at": s.created_at.isoformat() if s.created_at else None
        })
    
    return {"sessions": result}

@router.get("/pending")
def get_pending_sessions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get pending live session requests (module creator teachers only)"""
    if current_user.role != UserRole.TEACHER:
        raise HTTPException(status_code=403, detail="Teachers only")
    
    from ..models.channel import Channel
    from ..models.group import Group
    
    # Only show pending sessions for channels the teacher created
    sessions = db.query(LiveSession).join(Channel).join(Group).filter(
        Group.school_id == current_user.school_id,
        LiveSession.status == LiveSessionStatus.PENDING,
        Channel.created_by == current_user.id
    ).all()
    
    result = []
    for s in sessions:
        host = db.query(User).filter(User.id == s.host_id).first()
        channel = db.query(Channel).filter(Channel.id == s.channel_id).first()
        result.append({
            "id": s.id,
            "type": s.type.value,
            "title": s.title,
            "host_name": host.full_name if host else "Unknown",
            "channel_name": channel.name if channel else "Unknown",
            "created_at": s.created_at.isoformat() if s.created_at else None
        })
    
    return {"pending": result, "count": len(result)}

@router.post("/{session_id}/approve")
def approve_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Approve a live session request (module creator only)"""
    if current_user.role != UserRole.TEACHER:
        raise HTTPException(status_code=403, detail="Teachers only")
    
    session = db.query(LiveSession).filter(LiveSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Check if teacher is the module creator
    from ..models.channel import Channel
    channel = db.query(Channel).filter(Channel.id == session.channel_id).first()
    if channel.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Only module creator can approve sessions")
    
    session.status = LiveSessionStatus.APPROVED
    db.commit()
    
    return {"success": True, "message": "Session approved"}

@router.post("/{session_id}/reject")
def reject_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Reject a live session request (module creator only)"""
    if current_user.role != UserRole.TEACHER:
        raise HTTPException(status_code=403, detail="Teachers only")
    
    session = db.query(LiveSession).filter(LiveSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Check if teacher is the module creator
    from ..models.channel import Channel
    channel = db.query(Channel).filter(Channel.id == session.channel_id).first()
    if channel.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Only module creator can reject sessions")
    
    session.status = LiveSessionStatus.REJECTED
    db.commit()
    
    return {"success": True, "message": "Session rejected"}

@router.post("/{session_id}/start")
def start_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Start an approved live session"""
    session = db.query(LiveSession).filter(LiveSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Only host or module creator can start
    from ..models.channel import Channel
    channel = db.query(Channel).filter(Channel.id == session.channel_id).first()
    is_module_creator = current_user.role == UserRole.TEACHER and channel.created_by == current_user.id
    
    if session.host_id != current_user.id and not is_module_creator:
        raise HTTPException(status_code=403, detail="Only host or module creator can start session")
    
    if session.status != LiveSessionStatus.APPROVED:
        raise HTTPException(status_code=400, detail="Session must be approved first")
    
    session.status = LiveSessionStatus.ACTIVE
    session.started_at = datetime.now()
    db.commit()
    
    return {"success": True, "room_id": session.room_id}

@router.post("/{session_id}/end")
def end_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """End an active live session"""
    session = db.query(LiveSession).filter(LiveSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Only host or module creator can end
    from ..models.channel import Channel
    channel = db.query(Channel).filter(Channel.id == session.channel_id).first()
    is_module_creator = current_user.role == UserRole.TEACHER and channel.created_by == current_user.id
    
    if session.host_id != current_user.id and not is_module_creator:
        raise HTTPException(status_code=403, detail="Only host or module creator can end session")
    
    session.status = LiveSessionStatus.ENDED
    session.ended_at = datetime.now()
    db.commit()
    
    return {"success": True, "message": "Session ended"}

@router.delete("/cleanup")
def cleanup_sessions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Clean up all old/stuck sessions (module creator only)"""
    if current_user.role != UserRole.TEACHER:
        raise HTTPException(status_code=403, detail="Teachers only")
    
    from ..models.channel import Channel
    
    # End all active/approved sessions in channels the teacher created
    stuck_sessions = db.query(LiveSession).join(Channel).filter(
        LiveSession.status.in_([LiveSessionStatus.ACTIVE, LiveSessionStatus.APPROVED]),
        Channel.created_by == current_user.id
    ).all()
    
    for session in stuck_sessions:
        session.status = LiveSessionStatus.ENDED
        session.ended_at = datetime.now()
    
    db.commit()
    
    return {"success": True, "cleaned": len(stuck_sessions)}
