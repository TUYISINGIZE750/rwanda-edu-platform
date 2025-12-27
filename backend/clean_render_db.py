"""
Remove duplicate schools from Render production database
Run this script to clean duplicates on production
"""
import os
import sys
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

# Render database URL (replace with your actual Render PostgreSQL URL)
RENDER_DB_URL = os.getenv('RENDER_DATABASE_URL', 'postgresql://...')

if 'postgresql://' not in RENDER_DB_URL:
    print("ERROR: Set RENDER_DATABASE_URL environment variable")
    print("Get it from: https://dashboard.render.com -> Your Database -> Connection String")
    sys.exit(1)

# Import models
sys.path.insert(0, os.path.dirname(__file__))
from app.models.school import School

# Connect to Render database
engine = create_engine(RENDER_DB_URL)
Session = sessionmaker(bind=engine)
db = Session()

print("Connected to Render database")
print("="*60)

# Get all schools
all_schools = db.query(School).all()
print(f'Total schools: {len(all_schools)}')

# Find duplicates
seen = {}
duplicates = []

for s in all_schools:
    key = (s.name.strip().lower(), s.province.lower(), s.district.lower())
    if key in seen:
        duplicates.append(s.id)
        print(f'DUPLICATE: {s.name} in {s.district}')
    else:
        seen[key] = s.id

print("="*60)
print(f'Found {len(duplicates)} duplicates')

if duplicates:
    confirm = input(f'\nRemove {len(duplicates)} duplicates? (yes/no): ')
    if confirm.lower() == 'yes':
        for dup_id in duplicates:
            school = db.query(School).filter(School.id == dup_id).first()
            if school:
                db.delete(school)
        db.commit()
        print(f'Removed {len(duplicates)} duplicates!')
        print(f'Remaining: {db.query(School).count()} schools')
    else:
        print('Cancelled')
else:
    print('No duplicates found')

db.close()
