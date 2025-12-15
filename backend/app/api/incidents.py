from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from typing import List
from ..core.database import get_db
from ..models.incident import Incident, IncidentStatus, IncidentSeverity
from ..models.message import Message, MessageStatus
from ..models.user import User, UserRole
from ..schemas.incident import IncidentCreate, IncidentResponse
from ..services.auth_service import get_current_user

router = APIRouter(prefix="/flags", tags=["incidents"])

@router.post("/", response_model=IncidentResponse)
def flag_message(
    incident_data: IncidentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify message exists
    message = db.query(Message).filter(Message.id == incident_data.message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    # Check if already flagged by this user
    existing = db.query(Incident).filter(
        Incident.message_id == incident_data.message_id,
        Incident.reporter_id == current_user.id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="You already flagged this message")
    
    incident = Incident(
        message_id=incident_data.message_id,
        reporter_id=current_user.id,
        reason=incident_data.reason,
        severity=incident_data.severity
    )
    db.add(incident)
    
    # Auto-hide message if severity is high
    if incident_data.severity == IncidentSeverity.HIGH:
        message.status = MessageStatus.HIDDEN
    
    db.commit()
    db.refresh(incident)
    return incident

@router.get("/pending")
def get_pending_incidents(
    severity: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role not in [UserRole.TEACHER, UserRole.ADMIN]:
        raise HTTPException(status_code=403, detail="Only teachers and admins can review incidents")
    
    query = db.query(Incident).filter(Incident.status == IncidentStatus.PENDING)
    
    if severity:
        query = query.filter(Incident.severity == severity)
    
    incidents = query.order_by(Incident.severity.desc(), Incident.created_at.asc()).all()
    
    # Enrich with message and reporter details
    result = []
    for inc in incidents:
        message = db.query(Message).filter(Message.id == inc.message_id).first()
        reporter = db.query(User).filter(User.id == inc.reporter_id).first()
        message_author = db.query(User).filter(User.id == message.user_id).first()
        
        result.append({
            "id": inc.id,
            "message": {
                "id": message.id,
                "content": message.content,
                "author": {
                    "id": message_author.id,
                    "full_name": message_author.full_name,
                    "role": message_author.role.value
                },
                "created_at": message.created_at
            },
            "reporter": {
                "id": reporter.id,
                "full_name": reporter.full_name,
                "role": reporter.role.value
            },
            "reason": inc.reason,
            "severity": inc.severity.value,
            "created_at": inc.created_at
        })
    
    return result

@router.post("/{incident_id}/resolve")
def resolve_incident(
    incident_id: int,
    action: str,
    notes: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role not in [UserRole.TEACHER, UserRole.ADMIN]:
        raise HTTPException(status_code=403, detail="Only teachers and admins can resolve incidents")
    
    if action not in ["dismiss", "hide_message", "warn_user"]:
        raise HTTPException(status_code=400, detail="Invalid action")
    
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    
    if incident.status != IncidentStatus.PENDING:
        raise HTTPException(status_code=400, detail="Incident already resolved")
    
    incident.status = IncidentStatus.RESOLVED
    incident.resolved_at = datetime.utcnow()
    incident.resolved_by = current_user.id
    incident.resolution_notes = notes
    
    # Take action on message
    message = db.query(Message).filter(Message.id == incident.message_id).first()
    if action == "hide_message":
        message.status = MessageStatus.HIDDEN
    elif action == "warn_user":
        message.status = MessageStatus.HIDDEN
        # In production, send notification to user
    
    db.commit()
    
    return {
        "status": "success",
        "action_taken": action,
        "incident_status": incident.status.value
    }

@router.get("/my-reports")
def get_my_reports(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    incidents = db.query(Incident).filter(
        Incident.reporter_id == current_user.id
    ).order_by(Incident.created_at.desc()).all()
    
    result = []
    for inc in incidents:
        message = db.query(Message).filter(Message.id == inc.message_id).first()
        result.append({
            "id": inc.id,
            "message_content": message.content[:100] + "..." if len(message.content) > 100 else message.content,
            "reason": inc.reason,
            "severity": inc.severity.value,
            "status": inc.status.value,
            "created_at": inc.created_at,
            "resolved_at": inc.resolved_at
        })
    
    return result

@router.get("/stats")
def get_incident_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin only")
    
    stats = {
        "total_incidents": db.query(func.count(Incident.id)).scalar(),
        "pending_incidents": db.query(func.count(Incident.id)).filter(
            Incident.status == IncidentStatus.PENDING
        ).scalar(),
        "resolved_incidents": db.query(func.count(Incident.id)).filter(
            Incident.status == IncidentStatus.RESOLVED
        ).scalar(),
        "high_severity": db.query(func.count(Incident.id)).filter(
            Incident.severity == IncidentSeverity.HIGH
        ).scalar(),
        "medium_severity": db.query(func.count(Incident.id)).filter(
            Incident.severity == IncidentSeverity.MEDIUM
        ).scalar(),
        "low_severity": db.query(func.count(Incident.id)).filter(
            Incident.severity == IncidentSeverity.LOW
        ).scalar()
    }
    
    return stats
