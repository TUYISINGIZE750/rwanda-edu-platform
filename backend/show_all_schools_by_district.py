"""Show all schools grouped by Province and District"""
import sys
sys.path.insert(0, '.')

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.school import School
from collections import defaultdict

# Database connection
engine = create_engine('sqlite:///app.db')
Session = sessionmaker(bind=engine)
db = Session()

# Get all schools
schools = db.query(School).order_by(School.province, School.district, School.name).all()

# Group by province and district
grouped = defaultdict(lambda: defaultdict(list))
for school in schools:
    grouped[school.province][school.district].append(school)

print("=" * 80)
print("ALL TVET/TSS SCHOOLS BY PROVINCE AND DISTRICT")
print("=" * 80)
print()

total_schools = 0
for province in sorted(grouped.keys()):
    print(f"\n{'='*80}")
    print(f"PROVINCE: {province}")
    print(f"{'='*80}")
    
    province_total = 0
    for district in sorted(grouped[province].keys()):
        schools_in_district = grouped[province][district]
        province_total += len(schools_in_district)
        
        print(f"\n  District: {district}")
        print(f"  Schools: {len(schools_in_district)}")
        print(f"  {'-'*76}")
        
        for i, school in enumerate(schools_in_district, 1):
            trades_count = len(school.trades) if school.trades else 0
            print(f"    {i}. {school.name}")
            print(f"       Type: {school.type} | Category: {school.category}")
            print(f"       Trades: {trades_count}")
            if trades_count > 0 and trades_count <= 5:
                print(f"       - {', '.join(school.trades[:5])}")
            elif trades_count > 5:
                print(f"       - {', '.join(school.trades[:3])} ... (+{trades_count-3} more)")
            print()
    
    print(f"  Total schools in {province}: {province_total}")
    total_schools += province_total

print(f"\n{'='*80}")
print(f"TOTAL SCHOOLS IN DATABASE: {total_schools}")
print(f"{'='*80}")

db.close()
