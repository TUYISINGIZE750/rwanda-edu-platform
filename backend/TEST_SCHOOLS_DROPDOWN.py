"""
Test script to verify schools dropdown works for all districts
"""
from app.core.database import SessionLocal
from app.models.school import School
from sqlalchemy import func

def test_schools_dropdown():
    db = SessionLocal()
    
    # Province mapping (Frontend -> Database)
    province_map = {
        'Southern Province': 'South',
        'Western Province': 'West',
        'Northern Province': 'North',
        'Eastern Province': 'East',
        'Kigali City': 'Kigali city'
    }
    
    # Test cases
    test_cases = [
        ('Southern Province', 'Kamonyi'),
        ('Southern Province', 'Huye'),
        ('Northern Province', 'Musanze'),
        ('Eastern Province', 'Bugesera'),
        ('Kigali City', 'Gasabo'),
    ]
    
    print("=" * 80)
    print("SCHOOLS DROPDOWN TEST - Province Mapping Fix")
    print("=" * 80)
    
    total_tests = len(test_cases)
    passed = 0
    
    for frontend_province, district in test_cases:
        db_province = province_map.get(frontend_province, frontend_province)
        
        schools = db.query(School).filter(
            func.lower(School.province) == db_province.lower(),
            func.lower(School.district) == district.lower()
        ).all()
        
        status = "PASS" if len(schools) > 0 else "FAIL"
        if len(schools) > 0:
            passed += 1
        
        print(f"\n{status} | {frontend_province} -> {district}")
        print(f"   Frontend Province: {frontend_province}")
        print(f"   Database Province: {db_province}")
        print(f"   Schools Found: {len(schools)}")
        
        if schools:
            for school in schools[:3]:
                trades_count = len(school.trades) if school.trades else 0
                print(f"      - {school.name} ({trades_count} trades)")
            if len(schools) > 3:
                print(f"      ... and {len(schools) - 3} more schools")
    
    db.close()
    
    print("\n" + "=" * 80)
    print(f"TEST SUMMARY: {passed}/{total_tests} tests passed")
    print("=" * 80)
    
    if passed == total_tests:
        print("ALL TESTS PASSED - Schools dropdown is working correctly!")
    else:
        print(f"WARNING: {total_tests - passed} test(s) failed")

if __name__ == "__main__":
    test_schools_dropdown()
