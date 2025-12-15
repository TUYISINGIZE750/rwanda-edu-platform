"""Test the student dashboard API directly"""
import sys
sys.path.insert(0, '.')

from app.core.database import SessionLocal
from app.models.user import User
from app.models.group import Group
from app.models.group_member import GroupMember

db = SessionLocal()

# Get KAMANYOLA Isdore
student = db.query(User).filter(User.id == 97).first()
print(f"Student: {student.full_name} (ID: {student.id})")
print(f"School: {student.school_id}")

# Check memberships
memberships = db.query(GroupMember).filter(GroupMember.user_id == 97).all()
print(f"\nMemberships found: {len(memberships)}")
for m in memberships:
    print(f"  Group ID: {m.group_id}")

# Get groups via JOIN
groups = db.query(Group).join(
    GroupMember, Group.id == GroupMember.group_id
).filter(
    GroupMember.user_id == 97
).all()

print(f"\nGroups via JOIN: {len(groups)}")
for g in groups:
    print(f"  {g.id}: {g.name} (School: {g.school_id})")

db.close()
