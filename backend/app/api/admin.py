from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from datetime import datetime, timedelta
from typing import List, Optional
from pydantic import BaseModel
from ..core.database import get_db
from ..models.user import User, UserRole
from ..models.group import Group
from ..models.channel import Channel
from ..models.message import Message, MessageStatus
from ..models.dm_request import DMRequest, DMRequestStatus
from ..models.incident import Incident, IncidentStatus
from ..models.resource import Resource
from ..services.auth_service import get_current_user
from ..core.security import get_password_hash

class CreateUserRequest(BaseModel):
    email: str
    password: str
    full_name: str
    role: str
    school_id: int
    province: str
    district: str
    locale: str
    grade: Optional[int] = None

router = APIRouter(prefix="/admin", tags=["admin"])

def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

@router.get("/dashboard")
def get_admin_dashboard(
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    try:
        school_id = current_user.school_id
        now = datetime.utcnow()
        week_ago = now - timedelta(days=7)
        
        # User stats
        total_students = db.query(func.count(User.id)).filter(
            User.school_id == school_id,
            User.role == UserRole.STUDENT
        ).scalar() or 0
        
        total_teachers = db.query(func.count(User.id)).filter(
            User.school_id == school_id,
            User.role == UserRole.TEACHER
        ).scalar() or 0
        
        active_users_week = db.query(func.count(User.id)).filter(
            User.school_id == school_id,
            User.updated_at >= week_ago
        ).scalar() or 0
        
        # Group stats
        total_groups = db.query(func.count(Group.id)).filter(
            Group.school_id == school_id
        ).scalar() or 0
        
        # Message stats
        total_messages = db.query(func.count(Message.id)).join(Channel).join(Group).filter(
            Group.school_id == school_id
        ).scalar() or 0
        
        pending_messages = db.query(func.count(Message.id)).join(Channel).join(Group).filter(
            Group.school_id == school_id,
            Message.status == MessageStatus.PENDING
        ).scalar() or 0
        
        messages_this_week = db.query(func.count(Message.id)).join(Channel).join(Group).filter(
            Group.school_id == school_id,
            Message.created_at >= week_ago
        ).scalar() or 0
        
        # DM Request stats
        pending_dm_requests = db.query(func.count(DMRequest.id)).join(
            User, DMRequest.student_id == User.id
        ).filter(
            User.school_id == school_id,
            DMRequest.status == DMRequestStatus.PENDING
        ).scalar() or 0
        
        active_dm_windows = db.query(func.count(DMRequest.id)).join(
            User, DMRequest.student_id == User.id
        ).filter(
            User.school_id == school_id,
            DMRequest.status == DMRequestStatus.APPROVED,
            DMRequest.window_end > now
        ).scalar() or 0
        
        # Incident stats
        pending_incidents = db.query(func.count(Incident.id)).join(
            Message, Incident.message_id == Message.id
        ).join(Channel).join(Group).filter(
            Group.school_id == school_id,
            Incident.status == IncidentStatus.PENDING
        ).scalar() or 0
        
        # Resource stats
        total_resources = db.query(func.count(Resource.id)).join(User).filter(
            User.school_id == school_id
        ).scalar() or 0
        
        total_storage_mb = (db.query(func.sum(Resource.size)).join(User).filter(
            User.school_id == school_id
        ).scalar() or 0) / (1024 * 1024)
        
        return {
            "users": {
                "total_students": total_students,
                "total_teachers": total_teachers,
                "active_this_week": active_users_week
            },
            "groups": {
                "total": total_groups
            },
            "messages": {
                "total": total_messages,
                "pending_moderation": pending_messages,
                "this_week": messages_this_week
            },
            "dm_requests": {
                "pending": pending_dm_requests,
                "active_windows": active_dm_windows
            },
            "incidents": {
                "pending": pending_incidents
            },
            "resources": {
                "total": total_resources,
                "storage_mb": round(total_storage_mb, 2)
            }
        }
    except Exception as e:
        print(f"Admin dashboard error: {e}")
        import traceback
        traceback.print_exc()
        # Return zeros if any query fails
        return {
            "users": {
                "total_students": 0,
                "total_teachers": 0,
                "active_this_week": 0
            },
            "groups": {
                "total": 0
            },
            "messages": {
                "total": 0,
                "pending_moderation": 0,
                "this_week": 0
            },
            "dm_requests": {
                "pending": 0,
                "active_windows": 0
            },
            "incidents": {
                "pending": 0
            },
            "resources": {
                "total": 0,
                "storage_mb": 0.0
            }
        }

@router.get("/users")
def list_users(
    role: str = None,
    grade: int = None,
    search: str = None,
    limit: int = 100,
    offset: int = 0,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    query = db.query(User).filter(User.school_id == current_user.school_id)
    
    if role:
        query = query.filter(User.role == role)
    
    if grade:
        query = query.filter(User.grade == grade)
    
    if search:
        query = query.filter(
            or_(
                User.full_name.ilike(f"%{search}%"),
                User.email.ilike(f"%{search}%")
            )
        )
    
    users = query.order_by(User.created_at.desc()).offset(offset).limit(limit).all()
    
    return [{
        "id": u.id,
        "email": u.email,
        "full_name": u.full_name,
        "role": u.role.value,
        "grade": u.grade,
        "is_active": u.is_active,
        "locale": u.locale,
        "created_at": u.created_at,
        "updated_at": u.updated_at
    } for u in users]

@router.post("/users")
def create_user(
    request: CreateUserRequest,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    # Check if email exists
    if db.query(User).filter(User.email == request.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")
    
    user = User(
        email=request.email,
        hashed_password=get_password_hash(request.password),
        full_name=request.full_name,
        role=UserRole(request.role),
        school_id=current_user.school_id,
        province=current_user.province,
        district=current_user.district,
        grade=request.grade,
        locale=request.locale or "rw"
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "role": user.role.value
    }

@router.put("/users/{user_id}")
def update_user(
    user_id: int,
    full_name: str = None,
    is_active: int = None,
    grade: int = None,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.id == user_id,
        User.school_id == current_user.school_id
    ).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if full_name is not None:
        user.full_name = full_name
    
    if is_active is not None:
        user.is_active = is_active
    
    if grade is not None:
        user.grade = grade
    
    user.updated_at = datetime.utcnow()
    db.commit()
    
    return {"status": "success"}

@router.delete("/users/{user_id}")
def deactivate_user(
    user_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.id == user_id,
        User.school_id == current_user.school_id
    ).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.role == UserRole.ADMIN:
        raise HTTPException(status_code=400, detail="Cannot deactivate admin users")
    
    user.is_active = 0
    db.commit()
    
    return {"status": "success"}

@router.get("/activity/recent")
def get_recent_activity(
    hours: int = 24,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    try:
        since = datetime.utcnow() - timedelta(hours=hours)
        school_id = current_user.school_id
        
        # Recent messages
        recent_messages = db.query(Message).join(Channel).join(Group).filter(
            Group.school_id == school_id,
            Message.created_at >= since
        ).count()
        
        # Recent DM requests
        recent_dm_requests = db.query(DMRequest).join(
            User, DMRequest.student_id == User.id
        ).filter(
            User.school_id == school_id,
            DMRequest.created_at >= since
        ).count()
        
        # Recent incidents
        recent_incidents = db.query(Incident).join(
            Message, Incident.message_id == Message.id
        ).join(Channel).join(Group).filter(
            Group.school_id == school_id,
            Incident.created_at >= since
        ).count()
        
        # Recent resources
        recent_resources = db.query(Resource).join(User).filter(
            User.school_id == school_id,
            Resource.created_at >= since
        ).count()
        
        return {
            "period_hours": hours,
            "messages": recent_messages,
            "dm_requests": recent_dm_requests,
            "incidents": recent_incidents,
            "resources": recent_resources
        }
    except Exception as e:
        return {
            "period_hours": hours,
            "messages": 0,
            "dm_requests": 0,
            "incidents": 0,
            "resources": 0
        }

@router.get("/groups/manage")
def manage_groups(
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    groups = db.query(Group).filter(
        Group.school_id == current_user.school_id
    ).all()
    
    result = []
    for g in groups:
        channel_count = db.query(func.count(Channel.id)).filter(
            Channel.group_id == g.id
        ).scalar()
        
        message_count = db.query(func.count(Message.id)).join(Channel).filter(
            Channel.group_id == g.id
        ).scalar()
        
        result.append({
            "id": g.id,
            "name": g.name,
            "type": g.type.value,
            "grade": g.grade,
            "channel_count": channel_count,
            "message_count": message_count,
            "created_at": g.created_at
        })
    
    return result

@router.get("/reports/engagement")
def get_engagement_report(
    days: int = 7,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    since = datetime.utcnow() - timedelta(days=days)
    school_id = current_user.school_id
    
    # Most active students
    active_students = db.query(
        User.id,
        User.full_name,
        func.count(Message.id).label('message_count')
    ).join(Message, Message.user_id == User.id).join(Channel).join(Group).filter(
        User.school_id == school_id,
        User.role == UserRole.STUDENT,
        Message.created_at >= since
    ).group_by(User.id, User.full_name).order_by(
        func.count(Message.id).desc()
    ).limit(10).all()
    
    # Most active teachers
    active_teachers = db.query(
        User.id,
        User.full_name,
        func.count(Message.id).label('message_count')
    ).join(Message, Message.user_id == User.id).join(Channel).join(Group).filter(
        User.school_id == school_id,
        User.role == UserRole.TEACHER,
        Message.created_at >= since
    ).group_by(User.id, User.full_name).order_by(
        func.count(Message.id).desc()
    ).limit(10).all()
    
    # Most active channels
    active_channels = db.query(
        Channel.id,
        Channel.name,
        func.count(Message.id).label('message_count')
    ).join(Message).join(Group).filter(
        Group.school_id == school_id,
        Message.created_at >= since
    ).group_by(Channel.id, Channel.name).order_by(
        func.count(Message.id).desc()
    ).limit(10).all()
    
    return {
        "period_days": days,
        "top_students": [{"id": s.id, "name": s.full_name, "messages": s.message_count} for s in active_students],
        "top_teachers": [{"id": t.id, "name": t.full_name, "messages": t.message_count} for t in active_teachers],
        "top_channels": [{"id": c.id, "name": c.name, "messages": c.message_count} for c in active_channels]
    }

@router.get("/analytics/overview")
def get_analytics_overview(
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    school_id = current_user.school_id
    now = datetime.utcnow()
    
    # Daily stats for last 7 days
    daily_stats = []
    for i in range(6, -1, -1):
        day_start = (now - timedelta(days=i)).replace(hour=0, minute=0, second=0)
        day_end = day_start + timedelta(days=1)
        
        messages = db.query(func.count(Message.id)).join(Channel).join(Group).filter(
            Group.school_id == school_id,
            Message.created_at >= day_start,
            Message.created_at < day_end
        ).scalar()
        
        daily_stats.append({
            "date": day_start.strftime("%Y-%m-%d"),
            "messages": messages
        })
    
    # User growth
    total_users = db.query(func.count(User.id)).filter(User.school_id == school_id).scalar()
    users_this_month = db.query(func.count(User.id)).filter(
        User.school_id == school_id,
        User.created_at >= now.replace(day=1, hour=0, minute=0, second=0)
    ).scalar()
    
    return {
        "daily_activity": daily_stats,
        "total_users": total_users,
        "new_users_this_month": users_this_month
    }

@router.get("/moderation/pending")
def get_pending_moderation(
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    school_id = current_user.school_id
    
    # Pending messages
    pending_messages = db.query(Message).join(Channel).join(Group).filter(
        Group.school_id == school_id,
        Message.status == MessageStatus.PENDING
    ).order_by(Message.created_at.desc()).limit(50).all()
    
    # Pending incidents
    pending_incidents = db.query(Incident).join(
        Message, Incident.message_id == Message.id
    ).join(Channel).join(Group).filter(
        Group.school_id == school_id,
        Incident.status == IncidentStatus.PENDING
    ).order_by(Incident.created_at.desc()).limit(50).all()
    
    return {
        "messages": [{
            "id": m.id,
            "content": m.content,
            "user_id": m.user_id,
            "channel_id": m.channel_id,
            "created_at": m.created_at
        } for m in pending_messages],
        "incidents": [{
            "id": i.id,
            "message_id": i.message_id,
            "reporter_id": i.reporter_id,
            "reason": i.reason,
            "created_at": i.created_at
        } for i in pending_incidents]
    }

@router.post("/moderation/approve/{message_id}")
def approve_message(
    message_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    message = db.query(Message).join(Channel).join(Group).filter(
        Message.id == message_id,
        Group.school_id == current_user.school_id
    ).first()
    
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    message.status = MessageStatus.APPROVED
    db.commit()
    
    return {"status": "approved"}

@router.post("/moderation/reject/{message_id}")
def reject_message(
    message_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    message = db.query(Message).join(Channel).join(Group).filter(
        Message.id == message_id,
        Group.school_id == current_user.school_id
    ).first()
    
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    message.status = MessageStatus.REJECTED
    db.commit()
    
    return {"status": "rejected"}

@router.get("/settings")
def get_settings(
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    # Return school-level settings (mock for now)
    return {
        "school_name": "KAYENZI TVET SCHOOL",
        "moderation_enabled": True,
        "auto_approve_teachers": True,
        "dm_request_auto_approve": False,
        "max_file_size_mb": 10,
        "allowed_file_types": ["pdf", "doc", "docx", "jpg", "png"],
        "session_timeout_minutes": 60
    }

@router.put("/settings")
def update_settings(
    moderation_enabled: bool = None,
    auto_approve_teachers: bool = None,
    dm_request_auto_approve: bool = None,
    max_file_size_mb: int = None,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    # In production, save to a settings table
    return {"status": "success", "message": "Settings updated"}

@router.post("/backup/create")
def create_backup(
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    # Mock backup creation
    backup_id = f"backup_{current_user.school_id}_{int(datetime.utcnow().timestamp())}"
    
    return {
        "backup_id": backup_id,
        "status": "completed",
        "created_at": datetime.utcnow(),
        "size_mb": 45.2
    }

@router.get("/backup/list")
def list_backups(
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    # Mock backup list
    now = datetime.utcnow()
    return [
        {
            "id": f"backup_{current_user.school_id}_001",
            "created_at": now - timedelta(days=1),
            "size_mb": 45.2,
            "status": "completed"
        },
        {
            "id": f"backup_{current_user.school_id}_002",
            "created_at": now - timedelta(days=7),
            "size_mb": 43.8,
            "status": "completed"
        }
    ]
