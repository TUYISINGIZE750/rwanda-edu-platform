"""Seed data for Rwanda National Education Platform"""
from app.core.database import SessionLocal
from app.models.user import User, UserRole
from app.models.group import Group, GroupType
from app.models.channel import Channel, ChannelType
from app.core.security import get_password_hash
from real_schools_data import ALL_SCHOOLS

def seed_database():
    db = SessionLocal()
    
    schools = ALL_SCHOOLS  # 38 real schools from REB/TVET/TSS
    
    # Create admin, teachers and students for each school
    for school in schools:
        school_id = school["id"]
        
        # Create 1 admin per school
        admin = User(
            email=f"admin@school{school_id}.rw",
            hashed_password=get_password_hash("admin123"),
            full_name=f"Admin - {school['name']}",
            role=UserRole.ADMIN,
            school_id=school_id,
            locale="rw"
        )
        db.add(admin)
        
        # Create 5 teachers per school
        for i in range(1, 6):
            teacher = User(
                email=f"teacher{i}@school{school_id}.rw",
                hashed_password=get_password_hash("teacher123"),
                full_name=f"Teacher {i} - {school['name']}",
                role=UserRole.TEACHER,
                school_id=school_id,
                locale="rw"
            )
            db.add(teacher)
        
        # Create 50 students per school (10 per grade, S1-S5)
        for grade in range(1, 6):
            for i in range(1, 11):
                student = User(
                    email=f"student{grade}{i}@school{school_id}.rw",
                    hashed_password=get_password_hash("student123"),
                    full_name=f"Student {grade}-{i} - {school['name']}",
                    role=UserRole.STUDENT,
                    school_id=school_id,
                    grade=grade,
                    locale="rw"
                )
                db.add(student)
        
        # Create groups for each grade
        for grade in range(1, 6):
            group = Group(
                school_id=school_id,
                name=f"S{grade} - {school['name']}",
                type=GroupType.CLASS,
                grade=grade
            )
            db.add(group)
            db.flush()
            
            # Create channels for each group
            for channel_type in [ChannelType.ANNOUNCEMENTS, ChannelType.DISCUSSION, 
                                ChannelType.RESOURCES, ChannelType.OFFICE_HOURS]:
                channel = Channel(
                    group_id=group.id,
                    name=channel_type.value.replace("_", " ").title(),
                    type=channel_type
                )
                db.add(channel)
        
        # Create clubs
        clubs = ["Science Club", "Math Club", "Sports Team"]
        for club_name in clubs:
            club = Group(
                school_id=school_id,
                name=f"{club_name} - {school['name']}",
                type=GroupType.CLUB
            )
            db.add(club)
            db.flush()
            
            channel = Channel(
                group_id=club.id,
                name="Discussion",
                type=ChannelType.DISCUSSION
            )
            db.add(channel)
    
    db.commit()
    total_users = len(schools) * 56  # 56 users per school
    print(f"✅ Seeded {len(schools)} schools across Rwanda")
    print(f"✅ Total users: {total_users} (admins, teachers, students)")
    print("✅ Created class groups (S1-S5) and clubs with channels")
    print("\n📧 Login credentials:")
    print("   Admin: admin@school1.rw / admin123")
    print("   Teacher: teacher1@school1.rw / teacher123")
    print("   Student: student11@school1.rw / student123")
    print(f"\n🏫 Schools: REB ({len([s for s in schools if s.get('type') in ['Public', 'Private']])}), TVET (5), TSS (3)")
    db.close()

if __name__ == "__main__":
    seed_database()
