from app.core.database import SessionLocal
from app.models.school import School

db = SessionLocal()

print("Available Provinces and Districts:")
print("="*60)

provinces = db.query(School.province).distinct().all()
for (prov,) in provinces:
    print(f"\nProvince: '{prov}'")
    districts = db.query(School.district).filter(School.province == prov).distinct().all()
    for (dist,) in districts:
        count = db.query(School).filter(School.province == prov, School.district == dist).count()
        print(f"  - {dist}: {count} schools")

db.close()
