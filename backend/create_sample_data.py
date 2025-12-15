"""
Generate sample data for admin demonstration
Creates users, groups, channels, messages, and activities
"""
import sys
import os
from datetime import datetime, timedelta
import random

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.models.user import User, UserRole
from app.models.group import Group, GroupType
from app.models.channel import Channel
from app.models.message import Message, MessageStatus
from app.models.resource import Resource
from app.core.security import get_password_hash

def create_sample_data():
    db = SessionLocal()
    
    try:
        # Get the admin user's school
        admin = db.query(User).filter(User.email == "admin@test.com").first()
        if not admin:
            print("Admin user not found. Please run CREATE_TEST_USERS.py first")
            return
        
        school_id = admin.school_id
        province = admin.province
        district = admin.district
        
        print(f"Creating sample data for school_id: {school_id}")
        
        # Create sample teachers
        teachers = []
        teacher_names = [
            "Alice Johnson", "Bob Smith", "Carol Williams", "David Brown",
            "Emma Davis", "Frank Miller", "Grace Wilson", "Henry Moore"
        ]
        
        for i, name in enumerate(teacher_names):
            email = f"teacher{i+1}@kayenzi.edu"
            existing = db.query(User).filter(User.email == email).first()
            if not existing:
                teacher = User(
                    email=email,
                    hashed_password=get_password_hash("teacher123"),
                    full_name=name,
                    role=UserRole.TEACHER,
                    school_id=school_id,
                    province=province,
                    district=district,
                    locale="rw",
                    is_active=1
                )
                db.add(teacher)
                teachers.append(teacher)
                print(f"Created teacher: {name}")
        
        db.commit()
        
        # Refresh to get IDs
        for t in teachers:
            db.refresh(t)
        
        # Create sample students
        students = []
        first_names = ["John", "Mary", "Peter", "Sarah", "James", "Linda", "Michael", "Patricia",
                      "Robert", "Jennifer", "William", "Elizabeth", "David", "Susan", "Richard"]
        last_names = ["Mugisha", "Uwase", "Nkunda", "Mukamana", "Habimana", "Uwera", "Bizimana",
                     "Mukandori", "Niyonzima", "Uwineza", "Nsengimana", "Mukeshimana"]
        
        for i in range(50):
            first = random.choice(first_names)
            last = random.choice(last_names)
            email = f"student{i+1}@kayenzi.edu"
            existing = db.query(User).filter(User.email == email).first()
            if not existing:
                student = User(
                    email=email,
                    hashed_password=get_password_hash("student123"),
                    full_name=f"{first} {last}",
                    role=UserRole.STUDENT,
                    school_id=school_id,
                    province=province,
                    district=district,
                    grade=random.randint(1, 6),
                    selected_trade=random.choice(["Electronics", "Welding", "Automotive", "Construction"]),
                    locale="rw",
                    is_active=1
                )
                db.add(student)
                students.append(student)
        
        db.commit()
        print(f"Created {len(students)} students")
        
        # Refresh students
        for s in students:
            db.refresh(s)
        
        # Create sample groups
        groups = []
        group_data = [
            ("Electronics Level 1", GroupType.CLASS, 1),
            ("Electronics Level 2", GroupType.CLASS, 2),
            ("Welding Basics", GroupType.CLASS, 1),
            ("Automotive Level 3", GroupType.CLASS, 3),
            ("Construction Level 2", GroupType.CLASS, 2),
            ("Robotics Club", GroupType.CLUB, None),
            ("Football Team", GroupType.TEAM, None),
        ]
        
        for name, gtype, grade in group_data:
            existing = db.query(Group).filter(Group.name == name, Group.school_id == school_id).first()
            if not existing:
                group = Group(
                    name=name,
                    type=gtype,
                    grade=grade,
                    school_id=school_id
                )
                db.add(group)
                groups.append(group)
                print(f"Created group: {name}")
        
        db.commit()
        
        # Refresh groups
        for g in groups:
            db.refresh(g)
        
        # Create channels for each group
        from app.models.channel import ChannelType
        channels = []
        channel_data = [
            ("General", ChannelType.DISCUSSION),
            ("Announcements", ChannelType.ANNOUNCEMENTS),
            ("Questions", ChannelType.DISCUSSION),
            ("Resources", ChannelType.RESOURCES)
        ]
        
        for group in groups:
            for ch_name, ch_type in channel_data:
                existing = db.query(Channel).filter(
                    Channel.name == ch_name,
                    Channel.group_id == group.id
                ).first()
                if not existing:
                    channel = Channel(
                        name=ch_name,
                        type=ch_type,
                        group_id=group.id
                    )
                    db.add(channel)
                    channels.append(channel)
        
        db.commit()
        print(f"Created {len(channels)} channels")
        
        # Refresh channels
        for c in channels:
            db.refresh(c)
        
        # Create sample messages
        message_templates = [
            "Welcome to the channel!",
            "Does anyone have questions about today's lesson?",
            "Great work everyone!",
            "Don't forget about the assignment due next week.",
            "Can someone explain this concept?",
            "Thanks for the help!",
            "Looking forward to our next session.",
            "This is really interesting material.",
            "I have a question about the homework.",
            "See you all tomorrow!"
        ]
        
        messages_created = 0
        now = datetime.utcnow()
        
        for channel in channels[:10]:  # Only first 10 channels for demo
            # Create messages over the last 7 days
            for day in range(7):
                msg_count = random.randint(3, 8)
                for _ in range(msg_count):
                    user = random.choice(students + teachers)
                    created_at = now - timedelta(days=day, hours=random.randint(0, 23))
                    
                    message = Message(
                        content=random.choice(message_templates),
                        user_id=user.id,
                        channel_id=channel.id,
                        status=MessageStatus.APPROVED,
                        created_at=created_at
                    )
                    db.add(message)
                    messages_created += 1
        
        db.commit()
        print(f"Created {messages_created} messages")
        
        # Create sample resources
        resource_data = [
            ("Electronics Fundamentals", "PDF", "https://example.com/electronics.pdf"),
            ("Welding Safety Guide", "PDF", "https://example.com/welding.pdf"),
            ("Automotive Basics", "PPTX", "https://example.com/automotive.pptx"),
            ("Construction Materials", "DOCX", "https://example.com/construction.docx"),
            ("Circuit Design Tutorial", "PDF", "https://example.com/circuit.pdf"),
            ("Welding Techniques Video", "VIDEO", "https://example.com/welding.mp4")
        ]
        
        resources_created = 0
        for title, res_type, url in resource_data:
            if groups:
                teacher = random.choice(teachers) if teachers else admin
                group = random.choice(groups)
                resource = Resource(
                    title=title,
                    type=res_type,
                    url=url,
                    description=f"Educational resource: {title}",
                    teacher_id=teacher.id,
                    group_id=group.id,
                    created_at=now - timedelta(days=random.randint(1, 30))
                )
                db.add(resource)
                resources_created += 1
        
        db.commit()
        print(f"Created {resources_created} resources")
        
        print("\nSample data created successfully!")
        print(f"\nSummary:")
        print(f"- Teachers: {len(teachers)}")
        print(f"- Students: {len(students)}")
        print(f"- Groups: {len(groups)}")
        print(f"- Channels: {len(channels)}")
        print(f"- Messages: {messages_created}")
        print(f"- Resources: {resources_created}")
        
    except Exception as e:
        print(f"Error creating sample data: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    create_sample_data()
