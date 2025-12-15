"""Create sample messages for testing"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal
from app.models.message import Message, MessageStatus
from app.models.channel import Channel
from app.models.user import User
from app.models.direct_message import DirectMessage, DMStatus
from datetime import datetime, timedelta
import random

def create_sample_messages():
    db = SessionLocal()
    
    try:
        # Get some users
        students = db.query(User).filter(User.role == 'student').limit(3).all()
        teachers = db.query(User).filter(User.role == 'teacher').limit(2).all()
        
        if not students or not teachers:
            print("❌ No users found. Please register some users first.")
            return
        
        # Get some channels
        channels = db.query(Channel).limit(3).all()
        
        if not channels:
            print("❌ No channels found. Please create some groups first.")
            return
        
        print(f"✅ Found {len(students)} students, {len(teachers)} teachers, {len(channels)} channels")
        
        # Sample messages for group chat
        sample_messages = [
            "Hello everyone! 👋",
            "Can someone help me with the assignment?",
            "The deadline is tomorrow, right?",
            "Yes, it's due at 11:59 PM",
            "Thanks for the clarification!",
            "Does anyone have notes from last class?",
            "I can share mine after class",
            "That would be great, thank you!",
            "What time is the exam?",
            "It's at 9:00 AM in Room 101",
            "Don't forget to bring your ID card",
            "Good luck everyone! 🍀",
        ]
        
        # Create group messages
        print("\n📝 Creating group messages...")
        for i, channel in enumerate(channels):
            for j in range(5):
                user = random.choice(students + teachers)
                message = Message(
                    channel_id=channel.id,
                    user_id=user.id,
                    content=random.choice(sample_messages),
                    status=MessageStatus.APPROVED,
                    created_at=datetime.now() - timedelta(hours=random.randint(1, 48))
                )
                db.add(message)
            print(f"  ✓ Added 5 messages to channel: {channel.name}")
        
        # Create some pending messages
        print("\n⏳ Creating pending messages...")
        for channel in channels[:2]:
            for student in students[:2]:
                message = Message(
                    channel_id=channel.id,
                    user_id=student.id,
                    content=f"This is a pending message from {student.full_name}",
                    status=MessageStatus.PENDING,
                    created_at=datetime.now() - timedelta(minutes=random.randint(5, 60))
                )
                db.add(message)
        print(f"  ✓ Added 4 pending messages")
        
        # Create direct messages
        print("\n💬 Creating direct messages...")
        dm_messages = [
            "Hi! How are you?",
            "I'm good, thanks! How about you?",
            "I have a question about the homework",
            "Sure, what do you need help with?",
            "Can we meet after class?",
            "Yes, I'm free at 3 PM",
            "Perfect! See you then",
            "Looking forward to it!",
        ]
        
        # Student to student DMs
        if len(students) >= 2:
            for i in range(4):
                dm = DirectMessage(
                    sender_id=students[0].id,
                    receiver_id=students[1].id,
                    content=dm_messages[i * 2],
                    status=DMStatus.APPROVED,
                    created_at=datetime.now() - timedelta(hours=random.randint(1, 24))
                )
                db.add(dm)
                
                dm_reply = DirectMessage(
                    sender_id=students[1].id,
                    receiver_id=students[0].id,
                    content=dm_messages[i * 2 + 1],
                    status=DMStatus.APPROVED,
                    created_at=datetime.now() - timedelta(hours=random.randint(1, 24))
                )
                db.add(dm_reply)
            print(f"  ✓ Added conversation between {students[0].full_name} and {students[1].full_name}")
        
        # Student to teacher DMs (some pending)
        if students and teachers:
            for i in range(3):
                status = DMStatus.PENDING if i == 0 else DMStatus.APPROVED
                dm = DirectMessage(
                    sender_id=students[0].id,
                    receiver_id=teachers[0].id,
                    content=f"Hello teacher, I have a question about lesson {i+1}",
                    status=status,
                    created_at=datetime.now() - timedelta(hours=random.randint(1, 12))
                )
                db.add(dm)
            print(f"  ✓ Added messages from {students[0].full_name} to {teachers[0].full_name} (1 pending)")
        
        db.commit()
        
        print("\n" + "="*50)
        print("✅ Sample data created successfully!")
        print("="*50)
        print("\n📊 Summary:")
        print(f"  • Group messages: {len(channels) * 5}")
        print(f"  • Pending messages: 4")
        print(f"  • Direct messages: 11")
        print(f"  • Pending DMs: 1")
        print("\n🎉 You can now test the chat system!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Creating sample chat messages...")
    print("="*50)
    create_sample_messages()
