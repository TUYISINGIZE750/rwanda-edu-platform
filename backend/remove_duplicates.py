from app.core.database import SessionLocal
from app.models.school import School
from sqlalchemy import func

db = SessionLocal()

# Get all schools in Kamonyi
schools = db.query(School).filter(
    func.lower(School.province) == 'south',
    func.lower(School.district) == 'kamonyi'
).all()

print(f'Total schools in Kamonyi: {len(schools)}')
print()

# Find duplicates
seen = {}
duplicates = []

for s in schools:
    key = s.name.strip().lower()
    if key in seen:
        print(f'DUPLICATE: {s.name}')
        print(f'  Keep ID: {seen[key]} | Delete ID: {s.id}')
        duplicates.append(s.id)
    else:
        seen[key] = s.id
        print(f'UNIQUE: {s.name} (ID: {s.id})')

print(f'\nFound {len(duplicates)} duplicates to remove')

if duplicates:
    print('\nRemoving duplicates...')
    for dup_id in duplicates:
        school = db.query(School).filter(School.id == dup_id).first()
        if school:
            print(f'Deleting: {school.name} (ID: {school.id})')
            db.delete(school)
    
    db.commit()
    print('Duplicates removed!')
else:
    print('No duplicates found')

db.close()
