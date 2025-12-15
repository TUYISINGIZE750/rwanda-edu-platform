from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, UniqueConstraint
from sqlalchemy.orm import relationship
from ..core.database import Base

class Reaction(Base):
    __tablename__ = "reactions"
    
    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(Integer, ForeignKey("messages.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    emoji = Column(String(10), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    __table_args__ = (
        UniqueConstraint('message_id', 'user_id', 'emoji', name='unique_user_reaction'),
    )
    
    message = relationship("Message", backref="reactions_list")
    user = relationship("User", backref="user_reactions")
