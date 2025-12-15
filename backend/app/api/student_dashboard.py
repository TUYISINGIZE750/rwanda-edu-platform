"""Student Dashboard API - All features in one place"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from datetime import datetime, timedelta
from ..core.database import get_db
from ..models.user import User, UserRole
from ..models.group import Group
from ..models.channel import Channel
from ..models.message import Message, MessageStatus
from ..core.security import get_current_user
from fastapi import HTTPException

router = APIRouter(prefix="/student", tags=["student"])

@router.get("/dashboard")
def get_student_dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get complete student dashboard data"""
    
    if current_user.role != UserRole.STUDENT:
        return {"error": "Student only"}
    
    try:
        from ..models.group_member import GroupMember
    except Exception as e:
        print(f"Error importing GroupMember: {e}")
        raise HTTPException(status_code=500, detail=f"Import error: {str(e)}")
    
    try:
        # Auto-enroll: Find matching groups and add student if not already member
        all_groups = db.query(Group).filter(Group.school_id == current_user.school_id).all()
    except Exception as e:
        print(f"Error querying groups: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    for g in all_groups:
        name = (g.name or '').lower()
        dept = (g.department or '').lower()
        
        # Check level match
        level_ok = False
        if current_user.selected_level:
            for num in ['1', '2', '3', '4', '5', '6']:
                if num in current_user.selected_level.lower():
                    if f'l{num}' in name or f'level{num}' in name or f'level {num}' in name:
                        level_ok = True
                        break
        
        # Check trade match
        trade_ok = False
        if current_user.selected_trade:
            for word in current_user.selected_trade.lower().split():
                if len(word) > 2 and (word in name or word in dept):
                    trade_ok = True
                    break
        
        # Auto-enroll if matches
        if level_ok and trade_ok:
            existing = db.query(GroupMember).filter(
                GroupMember.group_id == g.id,
                GroupMember.user_id == current_user.id
            ).first()
            
            if not existing:
                new_member = GroupMember(group_id=g.id, user_id=current_user.id)
                db.add(new_member)
    
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error committing: {e}")
    
    # Get enrolled groups
    try:
        groups = db.query(Group).join(
            GroupMember, Group.id == GroupMember.group_id
        ).filter(
            GroupMember.user_id == current_user.id
        ).all()
    except Exception as e:
        print(f"Error getting enrolled groups: {e}")
        groups = []
    
    my_groups = []
    total_unread = 0
    
    for group in groups:
        # Get channels for this group
        channels = db.query(Channel).filter(Channel.group_id == group.id).all()
        
        # Count unread messages across all channels
        unread_count = 0
        for channel in channels:
            unread = db.query(func.count(Message.id)).filter(
                Message.channel_id == channel.id,
                Message.status == MessageStatus.APPROVED,
                Message.user_id != current_user.id
            ).scalar() or 0
            unread_count += unread
        
        total_unread += unread_count
        
        # Count members matching this group's level and trade
        member_query = db.query(func.count(User.id)).filter(
            User.school_id == group.school_id,
            User.role == UserRole.STUDENT
        )
        
        # Filter by level
        if group.name:
            name_lower = group.name.lower()
            for num in ['1', '2', '3', '4', '5', '6']:
                if f'l{num}' in name_lower or f'level{num}' in name_lower:
                    member_query = member_query.filter(User.selected_level.like(f'%{num}%'))
                    break
        
        # Filter by trade
        if group.department:
            dept_words = [w for w in group.department.lower().split() if len(w) > 2]
            if dept_words:
                filters = [User.selected_trade.like(f'%{w}%') for w in dept_words]
                member_query = member_query.filter(or_(*filters))
        elif group.name:
            name_words = [w for w in group.name.lower().split() if len(w) > 2 and w not in ['level', 'class']]
            if name_words:
                filters = [User.selected_trade.like(f'%{w}%') for w in name_words]
                member_query = member_query.filter(or_(*filters))
        
        member_count = member_query.scalar() or 0
        
        my_groups.append({
            "id": group.id,
            "name": group.name,
            "type": group.type.value if hasattr(group.type, 'value') else str(group.type),
            "member_count": member_count,
            "unread_count": unread_count,
            "channels_count": len(channels),
            "channels": [{
                "id": c.id,
                "name": c.name,
                "type": c.type.value if hasattr(c.type, 'value') else str(c.type)
            } for c in channels]
        })
    
    # 2. Get Resources from groups the student belongs to
    from ..models.resource import Resource
    
    resources = []
    for group in groups:
        group_resources = db.query(Resource).filter(
            Resource.group_id == group.id
        ).order_by(Resource.created_at.desc()).limit(5).all()
        
        for res in group_resources:
            teacher = db.query(User).filter(User.id == res.teacher_id).first()
            resources.append({
                "id": res.id,
                "title": res.title,
                "type": res.type,
                "url": res.url,
                "description": res.description,
                "group_id": group.id,
                "group_name": group.name,
                "uploaded_by": teacher.full_name if teacher else "Teacher",
                "uploaded_at": res.created_at.isoformat() if res.created_at else None
            })
    
    # 3. Get Active Sessions
    sessions = []
    
    return {
        "student_info": {
            "name": current_user.full_name,
            "email": current_user.email,
            "trade": current_user.selected_trade,
            "level": current_user.selected_level,
            "school_id": current_user.school_id
        },
        "stats": {
            "groups_count": len(my_groups),
            "unread_messages": total_unread,
            "resources_count": len(resources),
            "active_sessions": len(sessions)
        },
        "groups": my_groups,
        "resources": resources,
        "sessions": sessions
    }

@router.get("/groups")
def get_my_groups(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get student's groups with details"""
    from ..models.group_member import GroupMember
    
    # Auto-enroll in matching groups
    all_groups = db.query(Group).filter(Group.school_id == current_user.school_id).all()
    
    for g in all_groups:
        name = (g.name or '').lower()
        dept = (g.department or '').lower()
        
        level_ok = False
        if current_user.selected_level:
            for num in ['1', '2', '3', '4', '5', '6']:
                if num in current_user.selected_level.lower():
                    if f'l{num}' in name or f'level{num}' in name or f'level {num}' in name:
                        level_ok = True
                        break
        
        trade_ok = False
        if current_user.selected_trade:
            for word in current_user.selected_trade.lower().split():
                if len(word) > 2 and (word in name or word in dept):
                    trade_ok = True
                    break
        
        if level_ok and trade_ok:
            existing = db.query(GroupMember).filter(
                GroupMember.group_id == g.id,
                GroupMember.user_id == current_user.id
            ).first()
            
            if not existing:
                new_member = GroupMember(group_id=g.id, user_id=current_user.id)
                db.add(new_member)
    
    db.commit()
    
    groups = db.query(Group).join(
        GroupMember, Group.id == GroupMember.group_id
    ).filter(
        GroupMember.user_id == current_user.id
    ).all()
    
    result = []
    for group in groups:
        channels = db.query(Channel).filter(Channel.group_id == group.id).all()
        
        unread_count = 0
        for channel in channels:
            unread = db.query(func.count(Message.id)).filter(
                Message.channel_id == channel.id,
                Message.status == MessageStatus.APPROVED,
                Message.user_id != current_user.id
            ).scalar() or 0
            unread_count += unread
        
        member_query = db.query(func.count(User.id)).filter(
            User.school_id == group.school_id,
            User.role == UserRole.STUDENT
        )
        
        if group.name:
            name_lower = group.name.lower()
            for num in ['1', '2', '3', '4', '5', '6']:
                if f'l{num}' in name_lower or f'level{num}' in name_lower:
                    member_query = member_query.filter(User.selected_level.like(f'%{num}%'))
                    break
        
        if group.department:
            dept_words = [w for w in group.department.lower().split() if len(w) > 2]
            if dept_words:
                filters = [User.selected_trade.like(f'%{w}%') for w in dept_words]
                member_query = member_query.filter(or_(*filters))
        elif group.name:
            name_words = [w for w in group.name.lower().split() if len(w) > 2 and w not in ['level', 'class']]
            if name_words:
                filters = [User.selected_trade.like(f'%{w}%') for w in name_words]
                member_query = member_query.filter(or_(*filters))
        
        member_count = member_query.scalar() or 0
        
        result.append({
            "id": group.id,
            "name": group.name,
            "type": group.type.value if hasattr(group.type, 'value') else str(group.type),
            "member_count": member_count,
            "unread_count": unread_count,
            "channels": [{
                "id": c.id,
                "name": c.name,
                "type": c.type.value if hasattr(c.type, 'value') else str(c.type)
            } for c in channels]
        })
    
    return result

@router.get("/messages/unread")
def get_unread_messages(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get count of unread messages"""
    
    # Get all groups for this student's school
    groups = db.query(Group).filter(
        Group.school_id == current_user.school_id
    ).all()
    
    total_unread = 0
    unread_by_group = []
    
    for group in groups:
        channels = db.query(Channel).filter(Channel.group_id == group.id).all()
        group_unread = 0
        
        for channel in channels:
            unread = db.query(func.count(Message.id)).filter(
                Message.channel_id == channel.id,
                Message.status == MessageStatus.APPROVED,
                Message.user_id != current_user.id
            ).scalar() or 0
            group_unread += unread
        
        if group_unread > 0:
            unread_by_group.append({
                "group_id": group.id,
                "group_name": group.name,
                "unread_count": group_unread
            })
        
        total_unread += group_unread
    
    return {
        "total_unread": total_unread,
        "by_group": unread_by_group
    }

@router.get("/resources")
def get_my_resources(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get student's learning resources from their groups"""
    from ..models.resource import Resource
    
    # Get all groups for this student
    groups = db.query(Group).filter(
        Group.school_id == current_user.school_id
    ).all()
    
    resources = []
    for group in groups:
        group_resources = db.query(Resource).filter(
            Resource.group_id == group.id
        ).order_by(Resource.created_at.desc()).all()
        
        for res in group_resources:
            teacher = db.query(User).filter(User.id == res.teacher_id).first()
            resources.append({
                "id": res.id,
                "title": res.title,
                "type": res.type,
                "url": res.url,
                "description": res.description,
                "group_name": group.name,
                "group_id": group.id,
                "uploaded_by": teacher.full_name if teacher else "Teacher",
                "uploaded_at": res.created_at.isoformat() if res.created_at else None
            })
    
    return {
        "total": len(resources),
        "resources": resources
    }

@router.get("/sessions")
def get_active_sessions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get student's active learning sessions"""
    
    # Mock sessions based on student's trade
    sessions = []
    
    if current_user.selected_trade:
        sessions = [
            {
                "id": 1,
                "title": f"{current_user.selected_trade} - Practical Workshop",
                "instructor": "Mr. Instructor",
                "start_time": (datetime.now() + timedelta(hours=2)).isoformat(),
                "end_time": (datetime.now() + timedelta(hours=4)).isoformat(),
                "duration": "2 hours",
                "location": "Workshop A - Building 2",
                "status": "upcoming"
            },
            {
                "id": 2,
                "title": f"{current_user.selected_level} - Theory Class",
                "instructor": "Ms. Teacher",
                "start_time": (datetime.now() + timedelta(days=1, hours=9)).isoformat(),
                "end_time": (datetime.now() + timedelta(days=1, hours=11)).isoformat(),
                "duration": "2 hours",
                "location": "Classroom 101",
                "status": "scheduled"
            }
        ]
    
    return {
        "total": len(sessions),
        "sessions": sessions
    }

@router.get("/resources/{resource_id}")
def get_resource_details(
    resource_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get resource details for viewing/downloading"""
    from ..models.resource import Resource
    
    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    
    group = db.query(Group).filter(Group.id == resource.group_id).first()
    teacher = db.query(User).filter(User.id == resource.teacher_id).first()
    
    return {
        "id": resource.id,
        "title": resource.title,
        "type": resource.type,
        "url": resource.url,
        "description": resource.description,
        "group_name": group.name if group else "Unknown",
        "uploaded_by": teacher.full_name if teacher else "Teacher",
        "uploaded_at": resource.created_at.isoformat() if resource.created_at else None
    }
