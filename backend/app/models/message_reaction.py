from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from ..core.database import Base

class MessageReaction(Base):
    __tablename__ = "message_reactions"
    
    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(Integer, nullable=False, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    emoji = Column(String(10), nullable=False)  # 👍, ❤️, 😂, 🔥, 🎉
    created_at = Column(DateTime(timezone=True), server_default=func.now())
