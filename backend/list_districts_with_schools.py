"""List all districts that have schools"""
import sys
sys.path.insert(0, '.')

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.school import School

engine = create_engine('sqlite:///app.db')
Session = sessionmaker(bind=engine)
db = Session()

# Get unique province/district combinations
schools = db.query(School.province, School.district).distinct().order_by(School.province, School.district).all()

print("DISTRICTS WITH SCHOOLS:")
print("="*60)

current_province = None
for province, district in schools:
    if province != current_province:
        print(f"\nProvince: {province}")
        current_province = province
    
    # Count schools in this district
    count = db.query(School).filter(School.province == province, School.district == district).count()
    print(f"  - {district} ({count} schools)")

print("\n" + "="*60)
print(f"Total combinations: {len(schools)}")

db.close()
