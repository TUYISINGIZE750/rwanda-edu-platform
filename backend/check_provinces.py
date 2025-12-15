from app.core.database import SessionLocal
from app.models.school import School
from sqlalchemy import distinct

db = SessionLocal()

print("Database provinces:")
provinces = db.query(distinct(School.province)).all()
for p in provinces:
    print(f"- '{p[0]}'")

print("\nDistricts in 'South' province:")
districts = db.query(distinct(School.district)).filter(School.province == 'South').all()
for d in districts:
    print(f"- '{d[0]}'")

print("\nSchools in Kamonyi, South:")
schools = db.query(School).filter(
    School.province == 'South',
    School.district == 'KAMONYI'
).all()
for s in schools:
    print(f"- {s.name}")

db.close()