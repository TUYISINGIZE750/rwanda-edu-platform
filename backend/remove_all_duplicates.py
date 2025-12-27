from app.core.database import SessionLocal
from app.models.school import School

db = SessionLocal()

# Get all schools
all_schools = db.query(School).all()

print(f'Total schools in database: {len(all_schools)}')
print('='*60)

# Find duplicates by name
seen = {}
duplicates = []

for s in all_schools:
    key = (s.name.strip().lower(), s.province.lower(), s.district.lower())
    if key in seen:
        duplicates.append(s.id)
        print(f'DUPLICATE: {s.name} in {s.district}, {s.province}')
        print(f'  Keep ID: {seen[key]} | Delete ID: {s.id}')
    else:
        seen[key] = s.id

print('='*60)
print(f'Found {len(duplicates)} duplicates')

if duplicates:
    print('\nRemoving duplicates...')
    for dup_id in duplicates:
        school = db.query(School).filter(School.id == dup_id).first()
        if school:
            db.delete(school)
    
    db.commit()
    print(f'Removed {len(duplicates)} duplicate schools!')
    
    # Verify
    remaining = db.query(School).count()
    print(f'Remaining schools: {remaining}')
else:
    print('No duplicates found')

db.close()
