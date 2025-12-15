"""Check district name differences between location data and school data"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

from app.core.database import SessionLocal
from app.models.school import School
from app.api.locations import RWANDA_DATA

def check_district_names():
    """Compare district names in location data vs school data"""
    print("Checking district name differences...")
    
    # Get districts from location data
    location_districts = set()
    for province in RWANDA_DATA["provinces"]:
        for district in province["districts"]:
            location_districts.add(district["name"])
    
    # Get districts from school data
    db = SessionLocal()
    school_districts = set()
    schools = db.query(School.district).distinct().all()
    for (district,) in schools:
        school_districts.add(district)
    db.close()
    
    print(f"\nLocation districts ({len(location_districts)}):")
    for district in sorted(location_districts):
        print(f"  - {district}")
    
    print(f"\nSchool districts ({len(school_districts)}):")
    for district in sorted(school_districts):
        print(f"  - {district}")
    
    print(f"\nDistricts in schools but not in locations:")
    for district in school_districts - location_districts:
        print(f"  - {district}")
    
    print(f"\nDistricts in locations but not in schools:")
    for district in location_districts - school_districts:
        print(f"  - {district}")
    
    # Find case-insensitive matches
    print(f"\nPossible case mismatches:")
    for school_district in school_districts:
        for location_district in location_districts:
            if school_district.lower() == location_district.lower() and school_district != location_district:
                print(f"  - School: '{school_district}' vs Location: '{location_district}'")

if __name__ == "__main__":
    check_district_names()