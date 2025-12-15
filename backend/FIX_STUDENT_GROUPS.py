"""Fix groups and students to show data on student dashboard"""
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal
from app.models.user import User, UserRole
from app.models.group import Group

def fix_data():
    db = SessionLocal()
    
    try:
        # Update groups to have departments matching trades
        groups = db.query(Group).all()
        
        for group in groups:
            if "Electronics" in group.name:
                group.department = "Electronics"
            elif "Welding" in group.name:
                group.department = "Welding"
            elif "Automotive" in group.name:
                group.department = "Automotive"
            elif "Construction" in group.name:
                group.department = "Construction"
            # Clubs and teams have no department (accessible to all)
        
        db.commit()
        print(f"Updated {len(groups)} groups with departments")
        
        # Ensure all students have selected_trade
        students = db.query(User).filter(User.role == UserRole.STUDENT).all()
        
        for student in students:
            if not student.selected_trade:
                student.selected_trade = "Electronics"
            if not student.selected_level:
                student.selected_level = f"Level {student.grade or 1}"
        
        db.commit()
        print(f"Updated {len(students)} students with trades and levels")
        
        # Show summary
        print("\nGroups by department:")
        for dept in ["Electronics", "Welding", "Automotive", "Construction", None]:
            count = db.query(Group).filter(Group.department == dept).count()
            print(f"  {dept or 'No department'}: {count}")
        
        print("\nStudents by trade:")
        for trade in ["Electronics", "Welding", "Automotive", "Construction"]:
            count = db.query(User).filter(
                User.role == UserRole.STUDENT,
                User.selected_trade == trade
            ).count()
            print(f"  {trade}: {count}")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_data()
