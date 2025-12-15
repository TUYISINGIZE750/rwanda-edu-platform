"""Test student dashboard API"""
from sqlalchemy import create_engine, select, or_
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.models.group import Group
from app.models.user import User

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

# Get student
student = db.query(User).filter(User.full_name.like('%Anne%')).first()
print(f"Student: {student.full_name}, Trade: {student.selected_trade}, School: {student.school_id}")

# Test query
groups = db.query(Group).filter(
    Group.school_id == student.school_id,
    or_(Group.department == student.selected_trade, Group.department == None)
).all()

print(f"\nGroups found: {len(groups)}")
for g in groups:
    print(f"  - {g.name} (Department: {g.department})")

db.close()
