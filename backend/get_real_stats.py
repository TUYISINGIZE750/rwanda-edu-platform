"""Get real statistics from database"""
import sys
sys.path.insert(0, '.')

from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from app.models.school import School

engine = create_engine('sqlite:///app.db')
Session = sessionmaker(bind=engine)
db = Session()

# Total schools
total = db.query(School).count()

# By province
provinces = db.query(School.province, func.count(School.id)).group_by(School.province).all()

# By type
types = db.query(School.type, func.count(School.id)).group_by(School.type).all()

print(f"Total Schools: {total}")
print("\nBy Province:")
for province, count in provinces:
    print(f"  {province}: {count}")

print("\nBy Type:")
for school_type, count in types:
    print(f"  {school_type}: {count}")

db.close()
