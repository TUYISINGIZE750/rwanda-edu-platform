from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List
from pydantic import BaseModel
from datetime import datetime
from ..core.database import get_db
from ..models.notification import Notification, NotificationType
from ..models.user import User
from ..services.auth_service import get_current_user

router = APIRouter(prefix="/notifications", tags=["notifications"])

class NotificationResponse(BaseModel):
    id: int
    type: str
    title: str
    message: str
    link: str | None
    is_read: bool
    created_at: datetime
    related_id: int | None
    related_type: str | None
    
    class Config:
        from_attributes = True

class NotificationCreate(BaseModel):
    user_id: int
    type: NotificationType
    title: str
    message: str
    link: str | None = None
    related_id: int | None = None
    related_type: str | None = None

@router.get("/", response_model=List[NotificationResponse])
def get_notifications(
    limit: int = 50,
    unread_only: bool = False,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get notifications for current user"""
    query = db.query(Notification).filter(Notification.user_id == current_user.id)
    
    if unread_only:
        query = query.filter(Notification.is_read == False)
    
    notifications = query.order_by(desc(Notification.created_at)).limit(limit).all()
    return notifications

@router.get("/unread-count")
def get_unread_count(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get count of unread notifications"""
    count = db.query(Notification).filter(
        Notification.user_id == current_user.id,
        Notification.is_read == False
    ).count()
    return {"unread_count": count}

@router.put("/{notification_id}/read")
def mark_as_read(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mark a notification as read"""
    notification = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == current_user.id
    ).first()
    
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    notification.is_read = True
    db.commit()
    return {"status": "success"}

@router.put("/mark-all-read")
def mark_all_as_read(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mark all notifications as read"""
    db.query(Notification).filter(
        Notification.user_id == current_user.id,
        Notification.is_read == False
    ).update({"is_read": True})
    db.commit()
    return {"status": "success", "message": "All notifications marked as read"}

@router.delete("/{notification_id}")
def delete_notification(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a notification"""
    notification = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == current_user.id
    ).first()
    
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    db.delete(notification)
    db.commit()
    return {"status": "success"}

# Helper function to create notifications (used by other services)
def create_notification(
    db: Session,
    user_id: int,
    notification_type: NotificationType,
    title: str,
    message: str,
    link: str | None = None,
    related_id: int | None = None,
    related_type: str | None = None
):
    """Create a new notification"""
    notification = Notification(
        user_id=user_id,
        type=notification_type,
        title=title,
        message=message,
        link=link,
        related_id=related_id,
        related_type=related_type
    )
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification

def create_bulk_notifications(
    db: Session,
    user_ids: List[int],
    notification_type: NotificationType,
    title: str,
    message: str,
    link: str | None = None,
    related_id: int | None = None,
    related_type: str | None = None
):
    """Create notifications for multiple users"""
    notifications = []
    for user_id in user_ids:
        notification = Notification(
            user_id=user_id,
            type=notification_type,
            title=title,
            message=message,
            link=link,
            related_id=related_id,
            related_type=related_type
        )
        notifications.append(notification)
    
    db.bulk_save_objects(notifications)
    db.commit()
    return len(notifications)
