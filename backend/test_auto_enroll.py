"""Test auto-enrollment logic"""
import sys
sys.path.insert(0, '.')

from app.core.database import SessionLocal
from app.models.user import User
from app.models.group import Group
from app.models.group_member import GroupMember

db = SessionLocal()

# Get all Land surveying Level 3 students in school 63
students = db.query(User).filter(
    User.school_id == 63,
    User.selected_level.like('%3%'),
    User.selected_trade.like('%Land%')
).all()

print(f"Found {len(students)} Land surveying L3 students in school 63:")
for s in students:
    print(f"  - {s.full_name} (ID: {s.id})")

# Get matching groups
groups = db.query(Group).filter(Group.school_id == 63).all()

print(f"\nGroups in school 63:")
for g in groups:
    print(f"  - {g.name} (ID: {g.id})")

# Simulate auto-enrollment
for student in students:
    for g in groups:
        name = (g.name or '').lower()
        dept = (g.department or '').lower()
        
        level_ok = False
        if student.selected_level:
            for num in ['1', '2', '3', '4', '5', '6']:
                if num in student.selected_level.lower():
                    if f'l{num}' in name or f'level{num}' in name or f'level {num}' in name:
                        level_ok = True
                        break
        
        trade_ok = False
        if student.selected_trade:
            for word in student.selected_trade.lower().split():
                if len(word) > 2 and (word in name or word in dept):
                    trade_ok = True
                    break
        
        if level_ok and trade_ok:
            existing = db.query(GroupMember).filter(
                GroupMember.group_id == g.id,
                GroupMember.user_id == student.id
            ).first()
            
            if not existing:
                print(f"\nAuto-enrolling {student.full_name} in {g.name}")
                new_member = GroupMember(group_id=g.id, user_id=student.id)
                db.add(new_member)

db.commit()

# Verify
print("\n" + "="*60)
print("FINAL MEMBERSHIPS:")
print("="*60)
for student in students:
    memberships = db.query(Group).join(
        GroupMember, Group.id == GroupMember.group_id
    ).filter(
        GroupMember.user_id == student.id
    ).all()
    
    print(f"\n{student.full_name}:")
    for g in memberships:
        print(f"  - {g.name}")

db.close()
