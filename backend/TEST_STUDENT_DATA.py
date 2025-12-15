"""Test student dashboard data"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal
from app.models.user import User
from app.models.group import Group

db = SessionLocal()

# Find Joshua
user = db.query(User).filter(User.full_name.like('%Joshua%')).first()
if not user:
    user = db.query(User).filter(User.email.like('%Joshua%')).first()

if user:
    print(f"User: {user.email}")
    print(f"Name: {user.full_name}")
    print(f"School ID: {user.school_id}")
    print(f"Trade: {user.selected_trade}")
    
    # Get groups at this school
    groups = db.query(Group).filter(Group.school_id == user.school_id).all()
    print(f"\nGroups at school {user.school_id}: {len(groups)}")
    for g in groups:
        print(f"  - {g.name} (dept: {g.department})")
else:
    print("Joshua not found")

db.close()
