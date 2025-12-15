from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import datetime, timedelta
from typing import List
from ..core.database import get_db
from ..models.dm_request import DMRequest, DMRequestStatus
from ..models.user import User, UserRole
from ..schemas.dm_request import DMRequestCreate, DMRequestResponse, DMRequestApprove
from ..services.auth_service import get_current_user

router = APIRouter(prefix="/dm-requests", tags=["dm-requests"])

@router.post("/", response_model=DMRequestResponse)
def create_dm_request(
    request_data: DMRequestCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != UserRole.STUDENT:
        raise HTTPException(status_code=403, detail="Only students can request DMs")
    
    # Verify teacher exists and is from same school
    teacher = db.query(User).filter(
        User.id == request_data.teacher_id,
        User.role == UserRole.TEACHER
    ).first()
    
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    if teacher.school_id != current_user.school_id:
        raise HTTPException(status_code=403, detail="Can only request DM from teachers in your school")
    
    # Check for existing pending or active request
    existing = db.query(DMRequest).filter(
        DMRequest.student_id == current_user.id,
        DMRequest.teacher_id == request_data.teacher_id,
        or_(
            DMRequest.status == DMRequestStatus.PENDING,
            and_(
                DMRequest.status == DMRequestStatus.APPROVED,
                DMRequest.window_end > datetime.utcnow()
            )
        )
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="You already have an active request with this teacher")
    
    dm_request = DMRequest(
        student_id=current_user.id,
        teacher_id=request_data.teacher_id,
        topic=request_data.topic,
        reason=request_data.reason
    )
    db.add(dm_request)
    db.commit()
    db.refresh(dm_request)
    return dm_request

@router.get("/my-requests")
def get_my_requests(
    status: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role == UserRole.STUDENT:
        query = db.query(DMRequest).filter(DMRequest.student_id == current_user.id)
    elif current_user.role in [UserRole.TEACHER, UserRole.ADMIN]:
        query = db.query(DMRequest).filter(DMRequest.teacher_id == current_user.id)
    else:
        raise HTTPException(status_code=403, detail="Access denied")
    
    if status:
        query = query.filter(DMRequest.status == status)
    
    requests = query.order_by(DMRequest.created_at.desc()).all()
    
    # Enrich with user details
    result = []
    for req in requests:
        student = db.query(User).filter(User.id == req.student_id).first()
        teacher = db.query(User).filter(User.id == req.teacher_id).first()
        
        result.append({
            "id": req.id,
            "student": {"id": student.id, "full_name": student.full_name, "email": student.email},
            "teacher": {"id": teacher.id, "full_name": teacher.full_name, "email": teacher.email},
            "topic": req.topic,
            "reason": req.reason,
            "status": req.status.value,
            "window_start": req.window_start,
            "window_end": req.window_end,
            "is_active": req.window_end > datetime.utcnow() if req.window_end else False,
            "created_at": req.created_at,
            "reviewed_at": req.reviewed_at
        })
    
    return result

@router.get("/pending")
def get_pending_requests(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role not in [UserRole.TEACHER, UserRole.ADMIN]:
        raise HTTPException(status_code=403, detail="Only teachers can view pending requests")
    
    requests = db.query(DMRequest).filter(
        DMRequest.teacher_id == current_user.id,
        DMRequest.status == DMRequestStatus.PENDING
    ).order_by(DMRequest.created_at.asc()).all()
    
    # Enrich with student details
    result = []
    for req in requests:
        student = db.query(User).filter(User.id == req.student_id).first()
        result.append({
            "id": req.id,
            "student": {
                "id": student.id,
                "full_name": student.full_name,
                "email": student.email,
                "grade": student.grade
            },
            "topic": req.topic,
            "reason": req.reason,
            "created_at": req.created_at
        })
    
    return result

@router.post("/{request_id}/approve")
def approve_dm_request(
    request_id: int,
    approval: DMRequestApprove,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role not in [UserRole.TEACHER, UserRole.ADMIN]:
        raise HTTPException(status_code=403, detail="Only teachers can approve")
    
    dm_request = db.query(DMRequest).filter(DMRequest.id == request_id).first()
    if not dm_request:
        raise HTTPException(status_code=404, detail="Request not found")
    
    if dm_request.teacher_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only approve your own requests")
    
    if dm_request.status != DMRequestStatus.PENDING:
        raise HTTPException(status_code=400, detail="Request already reviewed")
    
    if approval.approved:
        if not approval.window_hours or approval.window_hours < 1 or approval.window_hours > 168:
            raise HTTPException(status_code=400, detail="Window hours must be between 1 and 168 (1 week)")
        
        dm_request.status = DMRequestStatus.APPROVED
        dm_request.window_start = datetime.utcnow()
        dm_request.window_end = datetime.utcnow() + timedelta(hours=approval.window_hours)
    else:
        dm_request.status = DMRequestStatus.REJECTED
    
    dm_request.reviewed_at = datetime.utcnow()
    db.commit()
    
    return {
        "status": "success",
        "request_status": dm_request.status.value,
        "window_start": dm_request.window_start,
        "window_end": dm_request.window_end
    }

@router.get("/active")
def get_active_dm_windows(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Get all active DM windows for current user
    now = datetime.utcnow()
    
    if current_user.role == UserRole.STUDENT:
        requests = db.query(DMRequest).filter(
            DMRequest.student_id == current_user.id,
            DMRequest.status == DMRequestStatus.APPROVED,
            DMRequest.window_end > now
        ).all()
    else:
        requests = db.query(DMRequest).filter(
            DMRequest.teacher_id == current_user.id,
            DMRequest.status == DMRequestStatus.APPROVED,
            DMRequest.window_end > now
        ).all()
    
    result = []
    for req in requests:
        other_user = db.query(User).filter(
            User.id == (req.teacher_id if current_user.role == UserRole.STUDENT else req.student_id)
        ).first()
        
        result.append({
            "id": req.id,
            "other_user": {
                "id": other_user.id,
                "full_name": other_user.full_name,
                "role": other_user.role.value
            },
            "topic": req.topic,
            "window_end": req.window_end,
            "time_remaining_hours": (req.window_end - now).total_seconds() / 3600
        })
    
    return result

@router.delete("/{request_id}")
def cancel_dm_request(
    request_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    dm_request = db.query(DMRequest).filter(DMRequest.id == request_id).first()
    if not dm_request:
        raise HTTPException(status_code=404, detail="Request not found")
    
    # Students can cancel their own pending requests
    if current_user.role == UserRole.STUDENT and dm_request.student_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    if dm_request.status != DMRequestStatus.PENDING:
        raise HTTPException(status_code=400, detail="Can only cancel pending requests")
    
    db.delete(dm_request)
    db.commit()
    
    return {"status": "success"}
