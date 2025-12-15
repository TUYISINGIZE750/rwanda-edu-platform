from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from typing import List
from datetime import datetime
from ..core.database import get_db
from ..models.group import Group, GroupType
from ..models.channel import Channel, ChannelType
from ..models.message import Message, MessageStatus
from ..models.user import User, UserRole
from ..core.security import get_current_user

router = APIRouter(prefix="/directory", tags=["groups"])

@router.get("/groups")
def get_user_groups(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Get groups based on user's school, grade, and attributes
    query = db.query(Group).filter(Group.school_id == current_user.school_id)
    
    # Filter by grade for students
    if current_user.role == UserRole.STUDENT and current_user.grade:
        query = query.filter(
            (Group.grade == current_user.grade) | (Group.grade == None)
        )
    
    # Filter by department/trade for TVET students
    if current_user.role == UserRole.STUDENT and current_user.selected_trade:
        query = query.filter(
            (Group.department == current_user.selected_trade) | (Group.department == None)
        )
    
    groups = query.all()
    
    # Add member count and unread count
    result = []
    for g in groups:
        member_count = db.query(func.count(User.id)).filter(
            User.school_id == g.school_id,
            User.grade == g.grade if g.grade else True
        ).scalar()
        
        result.append({
            "id": g.id,
            "name": g.name,
            "type": g.type.value,
            "grade": g.grade,
            "department": g.department,
            "member_count": member_count,
            "created_at": g.created_at
        })
    
    return result

@router.get("/groups/{group_id}")
def get_group_details(
    group_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    # Check if user is enrolled in this group or same school
    from ..models.group_member import GroupMember
    is_member = db.query(GroupMember).filter(
        GroupMember.group_id == group_id,
        GroupMember.user_id == current_user.id
    ).first()
    
    if not is_member and group.school_id != current_user.school_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Count members in this group using flexible matching
    query = db.query(func.count(User.id)).filter(
        User.school_id == group.school_id,
        User.role == UserRole.STUDENT
    )
    
    # Filter by level if group name contains level
    if group.name:
        name_lower = group.name.lower()
        for num in ['1', '2', '3', '4', '5', '6']:
            if f'l{num}' in name_lower or f'level{num}' in name_lower or f'level {num}' in name_lower:
                query = query.filter(User.selected_level.like(f'%{num}%'))
                break
    
    # Filter by trade if group has department or name contains trade keywords
    if group.department:
        dept_words = [w for w in group.department.lower().split() if len(w) > 2]
        if dept_words:
            filters = [User.selected_trade.like(f'%{w}%') for w in dept_words]
            query = query.filter(or_(*filters))
    elif group.name:
        name_words = [w for w in group.name.lower().split() if len(w) > 2 and w not in ['level', 'class']]
        if name_words:
            filters = [User.selected_trade.like(f'%{w}%') for w in name_words]
            query = query.filter(or_(*filters))
    
    member_count = query.scalar() or 0
    
    return {
        "id": group.id,
        "name": group.name,
        "type": group.type.value,
        "grade": group.grade,
        "department": group.department,
        "roster_source": group.roster_source,
        "member_count": member_count,
        "created_at": group.created_at
    }

@router.get("/groups/{group_id}/channels")
def get_group_channels(
    group_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group or group.school_id != current_user.school_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    channels = db.query(Channel).filter(Channel.group_id == group_id).all()
    
    result = []
    for c in channels:
        unread_count = db.query(func.count(Message.id)).filter(
            Message.channel_id == c.id,
            Message.status == MessageStatus.APPROVED,
            Message.created_at > (current_user.updated_at or current_user.created_at)
        ).scalar()
        
        # Check if teacher can access this channel
        can_access = True
        if current_user.role == UserRole.TEACHER:
            # Both class teachers and regular teachers can only access their own modules
            can_access = (c.created_by == current_user.id)
        
        result.append({
            "id": c.id,
            "name": c.name,
            "type": c.type.value,
            "unread_count": unread_count,
            "created_at": c.created_at,
            "created_by": c.created_by,
            "can_access": can_access
        })
    
    return result

@router.post("/groups/{group_id}/channels")
def create_channel(
    group_id: int,
    channel_data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != UserRole.TEACHER:
        raise HTTPException(status_code=403, detail="Only teachers can create channels")
    
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group or group.school_id != current_user.school_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Ensure teacher is a member of the group
    from ..models.group_member import GroupMember
    existing_member = db.query(GroupMember).filter(
        GroupMember.group_id == group_id,
        GroupMember.user_id == current_user.id
    ).first()
    
    if not existing_member:
        member = GroupMember(
            group_id=group_id,
            user_id=current_user.id
        )
        db.add(member)
    
    channel = Channel(
        name=channel_data["name"],
        type=ChannelType.DISCUSSION,
        group_id=group_id,
        created_by=current_user.id
    )
    
    db.add(channel)
    db.commit()
    db.refresh(channel)
    
    return {
        "id": channel.id,
        "name": channel.name,
        "type": channel.type.value,
        "message": "Module created successfully"
    }

@router.get("/groups/{group_id}/members")
def get_group_members(
    group_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role not in [UserRole.TEACHER, UserRole.ADMIN]:
        raise HTTPException(status_code=403, detail="Only teachers and admins can view members")
    
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group or group.school_id != current_user.school_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Get members based on school, level, and trade matching
    query = db.query(User).filter(
        User.school_id == group.school_id,
        User.role == UserRole.STUDENT
    )
    
    # Filter by level if group name contains level
    if group.name:
        name_lower = group.name.lower()
        for num in ['1', '2', '3', '4', '5', '6']:
            if f'l{num}' in name_lower or f'level{num}' in name_lower or f'level {num}' in name_lower:
                query = query.filter(User.selected_level.like(f'%{num}%'))
                break
    
    # Filter by trade if group has department or name contains trade keywords
    if group.department:
        dept_words = [w for w in group.department.lower().split() if len(w) > 2]
        if dept_words:
            filters = [User.selected_trade.like(f'%{w}%') for w in dept_words]
            query = query.filter(or_(*filters))
    elif group.name:
        name_words = [w for w in group.name.lower().split() if len(w) > 2 and w not in ['level', 'class']]
        if name_words:
            filters = [User.selected_trade.like(f'%{w}%') for w in name_words]
            query = query.filter(or_(*filters))
    
    members = query.all()
    return [{
        "id": m.id,
        "full_name": m.full_name,
        "email": m.email,
        "role": m.role.value if hasattr(m.role, 'value') else str(m.role),
        "selected_trade": m.selected_trade,
        "selected_level": m.selected_level
    } for m in members]

@router.get("/schools/{school_id}/stats")
def get_school_stats(
    school_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin only")
    
    if current_user.school_id != school_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    stats = {
        "total_students": db.query(func.count(User.id)).filter(
            User.school_id == school_id,
            User.role == UserRole.STUDENT
        ).scalar(),
        "total_teachers": db.query(func.count(User.id)).filter(
            User.school_id == school_id,
            User.role == UserRole.TEACHER
        ).scalar(),
        "total_groups": db.query(func.count(Group.id)).filter(
            Group.school_id == school_id
        ).scalar(),
        "total_messages": db.query(func.count(Message.id)).join(Channel).join(Group).filter(
            Group.school_id == school_id
        ).scalar(),
        "pending_messages": db.query(func.count(Message.id)).join(Channel).join(Group).filter(
            Group.school_id == school_id,
            Message.status == MessageStatus.PENDING
        ).scalar()
    }
    
    return stats

@router.post("/groups")
def create_group(
    group_data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role not in [UserRole.TEACHER, UserRole.ADMIN]:
        raise HTTPException(status_code=403, detail="Only teachers and admins can create groups")
    
    # Create the group
    group = Group(
        name=group_data["name"],
        type=group_data["type"],
        school_id=current_user.school_id,
        grade=group_data.get("grade"),
        department=group_data.get("department"),
        roster_source="manual",
        created_at=datetime.now()
    )
    
    db.add(group)
    db.commit()
    db.refresh(group)
    
    # Create default channels with teacher as creator
    default_channels = [
        Channel(name="Announcements", type=ChannelType.ANNOUNCEMENTS, group_id=group.id, created_by=current_user.id),
        Channel(name="Discussion", type=ChannelType.DISCUSSION, group_id=group.id, created_by=current_user.id),
        Channel(name="Resources", type=ChannelType.RESOURCES, group_id=group.id, created_by=current_user.id)
    ]
    
    for channel in default_channels:
        db.add(channel)
    
    db.commit()
    
    # Add teacher as member of the group
    from ..models.group_member import GroupMember
    teacher_member = GroupMember(
        group_id=group.id,
        user_id=current_user.id
    )
    db.add(teacher_member)
    db.commit()
    
    # Extract level from group name
    name_upper = group.name.upper()
    level = None
    for num in ['1', '2', '3', '4', '5', '6']:
        if f'L{num}' in name_upper or f'LEVEL {num}' in name_upper or f'LEVEL{num}' in name_upper:
            level = f'Level {num}'
            break
    
    # Extract trade keywords from name or department
    trade_keywords = []
    if group.department:
        trade_keywords = [w for w in group.department.split() if len(w) > 2]
    else:
        # Extract from name
        name_words = group.name.upper().split()
        trade_map = {
            'SWD': 'Software Development',
            'SOFTWARE': 'Software Development',
            'ELECTRONICS': 'Electronics',
            'ELECTRICAL': 'Electrical',
            'MECHANICAL': 'Mechanical',
            'CIVIL': 'Civil',
            'PLUMBING': 'Plumbing'
        }
        for word in name_words:
            if word in trade_map:
                trade_keywords.append(trade_map[word])
    
    # Only auto-assign if BOTH level AND trade are detected
    matching_students = []
    if level and trade_keywords:
        query = db.query(User).filter(
            User.school_id == group.school_id,
            User.role == UserRole.STUDENT,
            User.selected_level == level
        )
        
        filters = [User.selected_trade.ilike(f'%{keyword}%') for keyword in trade_keywords]
        query = query.filter(or_(*filters))
        
        matching_students = query.all()
    
    # Auto-assign matching students
    assigned_count = 0
    for student in matching_students:
        # Check if already a member
        existing = db.query(GroupMember).filter(
            GroupMember.group_id == group.id,
            GroupMember.user_id == student.id
        ).first()
        
        if not existing:
            member = GroupMember(
                group_id=group.id,
                user_id=student.id
            )
            db.add(member)
            assigned_count += 1
    
    db.commit()
    
    message = f"Group created successfully!"
    if level and trade_keywords:
        message += f" {assigned_count} students automatically assigned ({level} + {', '.join(trade_keywords)})."
    else:
        message += " No auto-assignment (level or trade not detected in name)."
    
    return {
        "id": group.id,
        "name": group.name,
        "type": group.type,
        "department": group.department,
        "students_assigned": assigned_count,
        "message": message
    }
