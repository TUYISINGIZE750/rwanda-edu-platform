"""Assign students to groups based on their grade/level"""
import sys
import os
import random

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal
from app.models.user import User, UserRole
from app.models.group import Group

def assign_students():
    db = SessionLocal()
    
    try:
        # Get all students
        students = db.query(User).filter(User.role == UserRole.STUDENT).all()
        
        # Get all groups
        groups = db.query(Group).all()
        
        if not students or not groups:
            print("No students or groups found")
            return
        
        print(f"Found {len(students)} students and {len(groups)} groups")
        
        # Create group_members table entries
        from sqlalchemy import text
        
        assigned = 0
        for student in students:
            # Assign to 2-3 random groups
            student_groups = random.sample(groups, min(random.randint(2, 3), len(groups)))
            
            for group in student_groups:
                # Check if already assigned
                check = db.execute(
                    text("SELECT 1 FROM group_members WHERE user_id = :uid AND group_id = :gid"),
                    {"uid": student.id, "gid": group.id}
                ).first()
                
                if not check:
                    db.execute(
                        text("INSERT INTO group_members (user_id, group_id) VALUES (:uid, :gid)"),
                        {"uid": student.id, "gid": group.id}
                    )
                    assigned += 1
        
        db.commit()
        print(f"Assigned {assigned} student-group memberships")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    assign_students()
