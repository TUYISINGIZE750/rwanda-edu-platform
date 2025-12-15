"""Add sample messages to existing channels"""
import sys
import os
from datetime import datetime, timedelta
import random

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.user import User, UserRole
from app.models.channel import Channel
from app.models.message import Message, MessageStatus

def add_messages():
    db = SessionLocal()
    
    try:
        # Get users
        students = db.query(User).filter(User.role == UserRole.STUDENT).limit(20).all()
        teachers = db.query(User).filter(User.role == UserRole.TEACHER).limit(5).all()
        
        if not students or not teachers:
            print("No users found")
            return
        
        # Get channels
        channels = db.query(Channel).limit(10).all()
        
        if not channels:
            print("No channels found")
            return
        
        print(f"Found {len(students)} students, {len(teachers)} teachers, {len(channels)} channels")
        
        # Message templates
        messages = [
            "Welcome to the channel!",
            "Does anyone have questions about today's lesson?",
            "Great work everyone!",
            "Don't forget about the assignment due next week.",
            "Can someone explain this concept?",
            "Thanks for the help!",
            "Looking forward to our next session.",
            "This is really interesting material.",
            "I have a question about the homework.",
            "See you all tomorrow!",
            "The practical session was very helpful.",
            "Could you share the notes from today?",
            "I'm working on the project now.",
            "When is the next exam?",
            "This topic is challenging but interesting."
        ]
        
        now = datetime.utcnow()
        created = 0
        
        for channel in channels:
            # Create messages over last 7 days
            for day in range(7):
                msg_count = random.randint(5, 12)
                for _ in range(msg_count):
                    user = random.choice(students + teachers)
                    created_at = now - timedelta(days=day, hours=random.randint(0, 23), minutes=random.randint(0, 59))
                    
                    msg = Message(
                        content=random.choice(messages),
                        user_id=user.id,
                        channel_id=channel.id,
                        status=MessageStatus.APPROVED,
                        created_at=created_at
                    )
                    db.add(msg)
                    created += 1
        
        db.commit()
        print(f"Created {created} messages successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_messages()
