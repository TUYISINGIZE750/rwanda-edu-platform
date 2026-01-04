"""Teacher Dashboard API"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
from typing import Optional
import os
import shutil
from datetime import datetime
from ..core.database import get_db
from ..models.user import User, UserRole
from ..models.group import Group, GroupType
from ..models.channel import Channel, ChannelType
from ..models.message import Message, MessageStatus
from ..core.security import get_current_user

router = APIRouter(prefix="/teacher", tags=["teacher"])

class CreateGroupRequest(BaseModel):
    name: str
    type: str
    department: Optional[str] = None
    grade: Optional[int] = None

@router.get("/dashboard")
def get_teacher_dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get teacher dashboard data"""
    try:
        if current_user.role != UserRole.TEACHER:
            raise HTTPException(status_code=403, detail="Teacher only")
        
        # Get groups based on teacher type
        from ..models.group_member import GroupMember
        
        print(f"Teacher: {current_user.full_name}, is_class_teacher: {current_user.is_class_teacher}, managed_class_id: {current_user.managed_class_id}")
        
        if current_user.is_class_teacher and current_user.managed_class_id:
            # Class teacher: only show their managed class
            groups = db.query(Group).filter(
                Group.id == current_user.managed_class_id
            ).all()
            print(f"Class teacher - showing {len(groups)} groups")
        else:
            # Regular teacher: show classes they have access to via GroupMember
            group_ids = db.query(GroupMember.group_id).filter(
                GroupMember.user_id == current_user.id
            ).distinct().all()
            group_ids = [gid[0] for gid in group_ids]
            
            if group_ids:
                groups = db.query(Group).filter(Group.id.in_(group_ids)).all()
            else:
                groups = []
            print(f"Regular teacher - showing {len(groups)} groups from {len(group_ids)} memberships")
        
        # Get students filtered by teacher's department
        if current_user.selected_trade:
            # Teacher has department - show only students in same department
            total_students = db.query(func.count(User.id)).filter(
                User.school_id == current_user.school_id,
                User.role == UserRole.STUDENT,
                User.selected_trade == current_user.selected_trade
            ).scalar() or 0
        else:
            # Teacher has no department - show all students
            total_students = db.query(func.count(User.id)).filter(
                User.school_id == current_user.school_id,
                User.role == UserRole.STUDENT
            ).scalar() or 0
        
        # Get resources uploaded by this teacher
        from ..models.resource import Resource
        resources = db.query(Resource).filter(
            Resource.teacher_id == current_user.id
        ).order_by(Resource.created_at.desc()).limit(10).all()
        
        resources_data = []
        for res in resources:
            resources_data.append({
                "id": res.id,
                "title": res.title,
                "type": res.type,
                "url": res.url,
                "group_id": res.group_id
            })
        
        groups_data = []
        for group in groups:
            member_count = db.query(func.count(User.id)).filter(
                User.school_id == group.school_id,
                User.role == UserRole.STUDENT
            ).scalar() or 0
            
            groups_data.append({
                "id": group.id,
                "name": group.name,
                "type": group.type.value,
                "member_count": member_count,
                "created_at": group.created_at.isoformat() if group.created_at else None
            })
        
        return {
            "teacher_info": {
                "name": current_user.full_name,
                "email": current_user.email,
                "school_id": current_user.school_id,
                "is_class_teacher": current_user.is_class_teacher,
                "can_create_groups": current_user.can_create_groups or current_user.is_class_teacher
            },
            "stats": {
                "groups_count": len(groups),
                "total_students": total_students,
                "pending_messages": 0,
                "resources_count": len(resources_data)
            },
            "groups": groups_data,
            "resources": resources_data,
            "sessions": []
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Dashboard error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/groups")
async def create_group(
    request: CreateGroupRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new group with auto-assignment based on department"""
    if current_user.role != UserRole.TEACHER:
        raise HTTPException(status_code=403, detail="Teacher only")
    
    # Check if teacher has permission to create groups
    if not current_user.is_class_teacher and not current_user.can_create_groups:
        raise HTTPException(
            status_code=403, 
            detail="You don't have permission to create classes/groups. Please contact your administrator."
        )
    
    try:
        group_type = GroupType(request.type.upper())
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid group type")
    
    group = Group(
        school_id=current_user.school_id,
        name=request.name,
        type=group_type,
        grade=request.grade,
        department=request.department
    )
    db.add(group)
    db.commit()
    db.refresh(group)
    
    default_channels = [
        Channel(group_id=group.id, name="Announcements", type=ChannelType.ANNOUNCEMENTS),
        Channel(group_id=group.id, name="Discussion", type=ChannelType.DISCUSSION),
        Channel(group_id=group.id, name="Resources", type=ChannelType.RESOURCES)
    ]
    
    for channel in default_channels:
        db.add(channel)
    
    db.commit()
    
    # AUTO-ASSIGN STUDENTS based on department match
    from ..models.group_member import GroupMember
    from ..models.notification import NotificationType
    from .notifications import create_notification
    
    assigned_count = 0
    
    if group.department:
        # Find students with matching department
        matching_students = db.query(User).filter(
            User.school_id == group.school_id,
            User.role == UserRole.STUDENT,
            User.selected_trade == group.department
        ).all()
        
        for student in matching_students:
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
                
                # Send notification to student
                await create_notification(
                    db=db,
                    user_id=student.id,
                    notification_type=NotificationType.CLASS_ASSIGNED,
                    title=f"Added to {group.name}",
                    message=f"You've been added to {group.name} by {current_user.full_name}",
                    link=f"/hubs/{group.id}",
                    related_id=group.id,
                    related_type="group"
                )
        
        db.commit()
    
    message = f"Group created successfully!"
    if group.department:
        message += f" {assigned_count} students auto-assigned from {group.department} department."
    else:
        message += " No department specified - no auto-assignment."
    
    return {
        "id": group.id,
        "name": group.name,
        "type": group.type.value,
        "department": group.department,
        "students_assigned": assigned_count,
        "message": message
    }

@router.put("/groups/{group_id}")
def update_group(
    group_id: int,
    request: CreateGroupRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a group"""
    if current_user.role != UserRole.TEACHER:
        raise HTTPException(status_code=403, detail="Teacher only")
    
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    if group.school_id != current_user.school_id:
        raise HTTPException(status_code=403, detail="Cannot edit groups from other schools")
    
    try:
        group_type = GroupType(request.type.upper())
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid group type")
    
    group.name = request.name
    group.type = group_type
    group.grade = request.grade
    
    db.commit()
    db.refresh(group)
    
    return {
        "id": group.id,
        "name": group.name,
        "type": group.type.value,
        "message": "Group updated successfully"
    }

@router.delete("/groups/{group_id}")
def delete_group(
    group_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a group"""
    try:
        if current_user.role != UserRole.TEACHER:
            raise HTTPException(status_code=403, detail="Teacher only")
        
        group = db.query(Group).filter(Group.id == group_id).first()
        if not group:
            raise HTTPException(status_code=404, detail="Group not found")
        
        if group.school_id != current_user.school_id:
            raise HTTPException(status_code=403, detail="Cannot delete groups from other schools")
        
        # Delete related channels first
        db.query(Channel).filter(Channel.group_id == group_id).delete()
        
        # Delete group members
        from ..models.group_member import GroupMember
        db.query(GroupMember).filter(GroupMember.group_id == group_id).delete()
        
        # Delete the group
        db.delete(group)
        db.commit()
        
        return {"message": "Group deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"Delete error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/groups/{group_id}/students")
def get_group_students(
    group_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get students in a group - filtered by teacher's department"""
    if current_user.role != UserRole.TEACHER:
        raise HTTPException(status_code=403, detail="Teacher only")
    
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    # Filter students by teacher's department
    query = db.query(User).filter(
        User.school_id == group.school_id,
        User.role == UserRole.STUDENT
    )
    
    if current_user.selected_trade:
        query = query.filter(User.selected_trade == current_user.selected_trade)
    
    students = query.all()
    
    return [{
        "id": s.id,
        "full_name": s.full_name,
        "email": s.email,
        "selected_trade": s.selected_trade,
        "selected_level": s.selected_level
    } for s in students]

@router.get("/students/{student_id}")
def get_student_profile(
    student_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get student profile"""
    if current_user.role != UserRole.TEACHER:
        raise HTTPException(status_code=403, detail="Teacher only")
    
    student = db.query(User).filter(User.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    return {
        "id": student.id,
        "full_name": student.full_name,
        "email": student.email,
        "role": student.role.value,
        "school_id": student.school_id,
        "province": student.province,
        "district": student.district,
        "selected_trade": student.selected_trade,
        "selected_level": student.selected_level,
        "created_at": student.created_at.isoformat() if student.created_at else None
    }

@router.get("/pending-messages")
def get_pending_messages(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all pending messages for moderation"""
    try:
        if current_user.role != UserRole.TEACHER:
            raise HTTPException(status_code=403, detail="Teacher only")
        
        groups = db.query(Group).filter(Group.school_id == current_user.school_id).all()
        
        pending = []
        for group in groups:
            channels = db.query(Channel).filter(Channel.group_id == group.id).all()
            for channel in channels:
                messages = db.query(Message).filter(
                    Message.channel_id == channel.id,
                    Message.status == MessageStatus.PENDING
                ).all()
                
                for msg in messages:
                    sender = db.query(User).filter(User.id == msg.user_id).first()
                    pending.append({
                        "id": msg.id,
                        "content": msg.content,
                        "sender": sender.full_name if sender else "Unknown",
                        "channel": channel.name,
                        "group": group.name,
                        "created_at": msg.created_at.isoformat() if msg.created_at else None
                    })
        
        return pending
    except HTTPException:
        raise
    except Exception as e:
        print(f"Pending messages error: {e}")
        return []

@router.post("/messages/{message_id}/approve")
def approve_message(
    message_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Approve a pending message"""
    if current_user.role != UserRole.TEACHER:
        raise HTTPException(status_code=403, detail="Teacher only")
    
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    message.status = MessageStatus.APPROVED
    db.commit()
    
    return {"message": "Message approved"}

@router.post("/messages/{message_id}/reject")
def reject_message(
    message_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Reject a pending message"""
    if current_user.role != UserRole.TEACHER:
        raise HTTPException(status_code=403, detail="Teacher only")
    
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    message.status = MessageStatus.REJECTED
    db.commit()
    
    return {"message": "Message rejected"}

class UploadResourceRequest(BaseModel):
    group_id: int
    title: str
    type: str
    url: Optional[str] = None
    description: Optional[str] = None

@router.get("/resources")
def get_teacher_resources(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all resources uploaded by teacher"""
    if current_user.role != UserRole.TEACHER:
        raise HTTPException(status_code=403, detail="Teacher only")
    
    from ..models.resource import Resource
    
    resources = db.query(Resource).filter(
        Resource.teacher_id == current_user.id
    ).order_by(Resource.created_at.desc()).all()
    
    result = []
    for res in resources:
        group = db.query(Group).filter(Group.id == res.group_id).first()
        result.append({
            "id": res.id,
            "title": res.title,
            "type": res.type,
            "url": res.url,
            "description": res.description,
            "group_name": group.name if group else "Unknown",
            "group_id": res.group_id,
            "created_at": res.created_at.isoformat() if res.created_at else None
        })
    
    return result

@router.post("/resources")
async def upload_resource(
    group_id: int = Form(...),
    title: str = Form(...),
    type: str = Form(...),
    description: Optional[str] = Form(None),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload a resource to a group - accepts all file types"""
    if current_user.role != UserRole.TEACHER:
        raise HTTPException(status_code=403, detail="Teacher only")
    
    from ..models.resource import Resource
    from ..models.group_member import GroupMember
    from ..models.notification import Notification, NotificationType
    
    # Create upload directory
    upload_dir = "uploads/resources"
    os.makedirs(upload_dir, exist_ok=True)
    
    # Generate unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_extension = os.path.splitext(file.filename)[1]
    safe_filename = f"{timestamp}_{file.filename.replace(' ', '_')}"
    file_path = os.path.join(upload_dir, safe_filename)
    
    # Save file
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
    
    # Get file size
    file_size = os.path.getsize(file_path)
    
    # Create resource URL
    file_url = f"/uploads/resources/{safe_filename}"
    
    resource = Resource(
        group_id=group_id,
        teacher_id=current_user.id,
        title=title,
        type=type,
        url=file_url,
        description=description,
        size=file_size
    )
    db.add(resource)
    db.commit()
    db.refresh(resource)
    
    # Get group name
    group = db.query(Group).filter(Group.id == group_id).first()
    group_name = group.name if group else "your class"
    
    # Create notifications for all students in the group
    student_ids = db.query(GroupMember.user_id).join(User).filter(
        GroupMember.group_id == group_id,
        User.role == UserRole.STUDENT
    ).all()
    
    notification_count = 0
    for (student_id,) in student_ids:
        notification = Notification(
            user_id=student_id,
            type=NotificationType.RESOURCE_UPLOADED,
            title=f"📚 New Resource: {title}",
            message=f"{current_user.full_name} uploaded a new {type} in {group_name}",
            link=f"/hubs/{group_id}",
            related_id=resource.id,
            related_type="resource"
        )
        db.add(notification)
        notification_count += 1
    
    db.commit()
    
    return {
        "id": resource.id,
        "title": resource.title,
        "url": file_url,
        "size": file_size,
        "message": f"Resource uploaded successfully! {notification_count} students notified."
    }

@router.put("/resources/{resource_id}")
async def update_resource(
    resource_id: int,
    group_id: int = Form(...),
    title: str = Form(...),
    type: str = Form(...),
    description: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a resource"""
    if current_user.role != UserRole.TEACHER:
        raise HTTPException(status_code=403, detail="Teacher only")
    
    from ..models.resource import Resource
    
    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    
    if resource.teacher_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only edit your own resources")
    
    # Handle new file upload
    if file:
        upload_dir = "uploads/resources"
        os.makedirs(upload_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_extension = os.path.splitext(file.filename)[1]
        filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join(upload_dir, filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        resource.url = f"http://localhost:8080/uploads/resources/{filename}"
    
    resource.title = title
    resource.type = type
    resource.description = description
    resource.group_id = group_id
    
    db.commit()
    db.refresh(resource)
    
    return {
        "id": resource.id,
        "title": resource.title,
        "url": resource.url,
        "message": "Resource updated successfully"
    }

@router.delete("/resources/{resource_id}")
def delete_resource(
    resource_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a resource"""
    if current_user.role != UserRole.TEACHER:
        raise HTTPException(status_code=403, detail="Teacher only")
    
    from ..models.resource import Resource
    
    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    
    if resource.teacher_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only delete your own resources")
    
    db.delete(resource)
    db.commit()
    
    return {"message": "Resource deleted successfully"}

@router.get("/resources/{resource_id}")
def get_resource_details(
    resource_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get resource details"""
    if current_user.role != UserRole.TEACHER:
        raise HTTPException(status_code=403, detail="Teacher only")
    
    from ..models.resource import Resource
    
    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    
    group = db.query(Group).filter(Group.id == resource.group_id).first()
    
    return {
        "id": resource.id,
        "title": resource.title,
        "type": resource.type,
        "url": resource.url,
        "description": resource.description,
        "group_id": resource.group_id,
        "group_name": group.name if group else "Unknown",
        "created_at": resource.created_at.isoformat() if resource.created_at else None
    }


@router.get("/students")
def get_department_students(
    department: Optional[str] = None,
    level: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all students in teacher's school filtered by department and level"""
    if current_user.role != UserRole.TEACHER:
        raise HTTPException(status_code=403, detail="Teacher only")
    
    query = db.query(User).filter(
        User.school_id == current_user.school_id,
        User.role == UserRole.STUDENT
    )
    
    # Apply filters
    if department:
        query = query.filter(User.selected_trade == department)
    elif current_user.selected_trade:
        # Default to teacher's department if no filter specified
        query = query.filter(User.selected_trade == current_user.selected_trade)
    
    if level:
        query = query.filter(User.selected_level == level)
    
    students = query.order_by(User.selected_level, User.full_name).all()
    
    return [{
        "id": s.id,
        "full_name": s.full_name,
        "email": s.email,
        "selected_trade": s.selected_trade,
        "selected_level": s.selected_level,
        "grade": s.grade,
        "province": s.province,
        "district": s.district,
        "created_at": s.created_at.isoformat() if s.created_at else None
    } for s in students]

@router.get("/school-info")
def get_school_info(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get teacher's school details with statistics"""
    if current_user.role != UserRole.TEACHER:
        raise HTTPException(status_code=403, detail="Teacher only")
    
    from ..models.school import School
    
    school = db.query(School).filter(School.id == current_user.school_id).first()
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    
    # Get statistics
    total_students = db.query(func.count(User.id)).filter(
        User.school_id == current_user.school_id,
        User.role == UserRole.STUDENT
    ).scalar() or 0
    
    total_teachers = db.query(func.count(User.id)).filter(
        User.school_id == current_user.school_id,
        User.role == UserRole.TEACHER
    ).scalar() or 0
    
    total_groups = db.query(func.count(Group.id)).filter(
        Group.school_id == current_user.school_id
    ).scalar() or 0
    
    # Get students by department
    students_by_dept = db.query(
        User.selected_trade,
        func.count(User.id).label('count')
    ).filter(
        User.school_id == current_user.school_id,
        User.role == UserRole.STUDENT,
        User.selected_trade.isnot(None)
    ).group_by(User.selected_trade).all()
    
    # Get students by level
    students_by_level = db.query(
        User.selected_level,
        func.count(User.id).label('count')
    ).filter(
        User.school_id == current_user.school_id,
        User.role == UserRole.STUDENT,
        User.selected_level.isnot(None)
    ).group_by(User.selected_level).all()
    
    return {
        "school": {
            "id": school.id,
            "name": school.name,
            "school_code": getattr(school, 'school_code', None),
            "type": school.type,
            "category": school.category,
            "province": school.province,
            "district": school.district,
            "gender": getattr(school, 'gender', None),
            "trades": school.trades if school.trades else []
        },
        "statistics": {
            "total_students": total_students,
            "total_teachers": total_teachers,
            "total_groups": total_groups,
            "students_by_department": [{"department": dept, "count": count} for dept, count in students_by_dept],
            "students_by_level": [{"level": level, "count": count} for level, count in students_by_level]
        }
    }

class CreateLessonRequest(BaseModel):
    group_id: int
    title: str
    description: Optional[str] = None

@router.post("/modules")
async def create_lesson(
    request: CreateLessonRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a lesson/module in a class"""
    if current_user.role != UserRole.TEACHER:
        raise HTTPException(status_code=403, detail="Teacher only")
    
    # Verify group exists and teacher has access
    group = db.query(Group).filter(Group.id == request.group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Class not found")
    
    if group.school_id != current_user.school_id:
        raise HTTPException(status_code=403, detail="Cannot add lessons to other schools' classes")
    
    # Create lesson as a channel in the group
    lesson_channel = Channel(
        group_id=request.group_id,
        name=request.title,
        type=ChannelType.DISCUSSION,
        description=request.description
    )
    db.add(lesson_channel)
    db.commit()
    db.refresh(lesson_channel)
    
    # Notify students in the class
    from ..models.group_member import GroupMember
    from ..models.notification import NotificationType
    from .notifications import create_notification
    
    student_ids = db.query(GroupMember.user_id).join(User).filter(
        GroupMember.group_id == request.group_id,
        User.role == UserRole.STUDENT
    ).all()
    
    for (student_id,) in student_ids:
        await create_notification(
            db=db,
            user_id=student_id,
            notification_type=NotificationType.RESOURCE_UPLOADED,
            title=f"📚 New Lesson: {request.title}",
            message=f"{current_user.full_name} added a new lesson in {group.name}",
            link=f"/hubs/{group.id}",
            related_id=lesson_channel.id,
            related_type="channel"
        )
    
    return {
        "id": lesson_channel.id,
        "title": lesson_channel.name,
        "group_id": request.group_id,
        "message": f"Lesson created successfully! {len(student_ids)} students notified."
    }
