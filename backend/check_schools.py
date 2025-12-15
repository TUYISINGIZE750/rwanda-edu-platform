"""Check what's in the database"""
from app.core.database import SessionLocal
from app.models.school import School

db = SessionLocal()

schools = db.query(School).limit(10).all()

print("Sample schools in database:")
print("="*60)
for s in schools:
    print(f"Province: '{s.province}'")
    print(f"District: '{s.district}'")
    print(f"Name: {s.name}")
    print(f"Trades: {s.trades}")
    print("-"*60)

# Get unique provinces
provinces = db.query(School.province).distinct().all()
print("\nUnique Provinces:")
for (p,) in provinces:
    print(f"  - '{p}'")

# Get districts for first province
if provinces:
    first_prov = provinces[0][0]
    districts = db.query(School.district).filter(School.province == first_prov).distinct().all()
    print(f"\nDistricts in '{first_prov}':")
    for (d,) in districts:
        print(f"  - '{d}'")

db.close()
