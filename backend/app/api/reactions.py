from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from ..core.database import get_db
from ..models.user import User
from ..models.message import Message
from ..models.reaction import Reaction
from ..core.security import get_current_user

router = APIRouter(prefix="/reactions", tags=["reactions"])

class ReactionRequest(BaseModel):
    message_id: int
    emoji: str

@router.post("/")
def add_reaction(
    request: ReactionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add or remove a reaction to a message (toggle)"""
    existing = db.query(Reaction).filter(
        Reaction.message_id == request.message_id,
        Reaction.user_id == current_user.id,
        Reaction.emoji == request.emoji
    ).first()
    
    if existing:
        # Remove reaction (toggle off)
        db.delete(existing)
        db.commit()
        return {"success": True, "action": "removed"}
    
    # Add reaction
    new_reaction = Reaction(
        message_id=request.message_id,
        user_id=current_user.id,
        emoji=request.emoji
    )
    db.add(new_reaction)
    db.commit()
    
    return {"success": True, "action": "added"}

@router.get("/channel/{channel_id}")
def get_channel_reactions(
    channel_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all reactions for messages in a channel"""
    messages = db.query(Message).filter(Message.channel_id == channel_id).all()
    msg_ids = [m.id for m in messages]
    
    reactions = db.query(Reaction).filter(Reaction.message_id.in_(msg_ids)).all()
    
    result = {}
    for msg_id in msg_ids:
        msg_reactions = [r for r in reactions if r.message_id == msg_id]
        user_reactions = [r.emoji for r in msg_reactions if r.user_id == current_user.id]
        
        # Count all emojis
        all_reactions = {}
        for r in msg_reactions:
            all_reactions[r.emoji] = all_reactions.get(r.emoji, 0) + 1
        
        result[msg_id] = {
            "likes": sum(1 for r in msg_reactions if r.emoji == "👍"),
            "loves": sum(1 for r in msg_reactions if r.emoji == "❤️"),
            "all_reactions": all_reactions,
            "user_reactions": user_reactions
        }
    
    return result
