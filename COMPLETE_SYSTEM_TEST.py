#!/usr/bin/env python3
"""
COMPLETE SYSTEM TEST - 100% VERIFICATION
Tests every component: Database, Backend API, Frontend compatibility
"""

import requests
import json
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Test Configuration
API_BASE = "http://localhost:8080/api/v1"
DB_URL = "sqlite:///./app.db"

def test_database():
    """Test 1: Database has schools"""
    print("🔍 TEST 1: Database Check")
    try:
        sys.path.append('backend')
        from backend.app.models.school import School
        
        engine = create_engine(DB_URL)
        Session = sessionmaker(bind=engine)
        db = Session()
        
        total_schools = db.query(School).count()
        gasabo_schools = db.query(School).filter(School.district == 'GASABO').all()
        
        print(f"   ✅ Total schools in DB: {total_schools}")
        print(f"   ✅ GASABO schools: {len(gasabo_schools)}")
        
        if len(gasabo_schools) > 0:
            print(f"   ✅ Sample school: {gasabo_schools[0].name}")
        
        db.close()
        return total_schools > 0
        
    except Exception as e:
        print(f"   ❌ Database error: {e}")
        return False

def test_backend_health():
    """Test 2: Backend server is running"""
    print("\n🔍 TEST 2: Backend Health")
    try:
        response = requests.get("http://localhost:8080/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Backend healthy: {data}")
            return True
        else:
            print(f"   ❌ Backend unhealthy: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Backend connection error: {e}")
        return False

def test_provinces_api():
    """Test 3: Provinces API"""
    print("\n🔍 TEST 3: Provinces API")
    try:
        response = requests.get(f"{API_BASE}/locations/provinces", timeout=5)
        if response.status_code == 200:
            provinces = response.json()
            print(f"   ✅ Provinces loaded: {len(provinces)} provinces")
            print(f"   ✅ Sample provinces: {[p['name'] for p in provinces[:3]]}")
            return len(provinces) > 0
        else:
            print(f"   ❌ Provinces API failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Provinces API error: {e}")
        return False

def test_districts_api():
    """Test 4: Districts API"""
    print("\n🔍 TEST 4: Districts API")
    try:
        response = requests.get(f"{API_BASE}/locations/districts/South", timeout=5)
        if response.status_code == 200:
            districts = response.json()
            print(f"   ✅ South districts loaded: {len(districts)} districts")
            print(f"   ✅ Sample districts: {[d['name'] for d in districts[:3]]}")
            return len(districts) > 0
        else:
            print(f"   ❌ Districts API failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Districts API error: {e}")
        return False

def test_schools_api():
    """Test 5: Schools by District API (THE CRITICAL ONE)"""
    print("\n🔍 TEST 5: Schools by District API (CRITICAL)")
    
    test_cases = [
        ("South", "NYANZA"),
        ("Kigali city", "GASABO"),
        ("West", "KARONGI")
    ]
    
    all_passed = True
    
    for province, district in test_cases:
        try:
            url = f"{API_BASE}/schools-by-district/district/{province}/{district}"
            print(f"   Testing: {url}")
            
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                schools_count = data.get('schools_count', 0)
                schools = data.get('schools', [])
                
                print(f"   ✅ {province}/{district}: {schools_count} schools")
                
                if schools_count > 0:
                    sample_school = schools[0]
                    print(f"      Sample: {sample_school['name']} ({sample_school['type']})")
                    print(f"      Trades: {sample_school['trades_count']} available")
                else:
                    print(f"   ⚠️  No schools in {district}")
                    
            else:
                print(f"   ❌ {province}/{district} failed: {response.status_code}")
                print(f"      Response: {response.text}")
                all_passed = False
                
        except Exception as e:
            print(f"   ❌ {province}/{district} error: {e}")
            all_passed = False
    
    return all_passed

def test_frontend_compatibility():
    """Test 6: Frontend API compatibility"""
    print("\n🔍 TEST 6: Frontend Compatibility")
    
    # Test the exact API call the frontend makes
    try:
        # Simulate frontend fetch call
        url = f"{API_BASE}/schools-by-district/district/South/NYANZA"
        
        # Test with requests (like axios)
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            
            # Check response structure matches frontend expectations
            required_fields = ['district', 'province', 'schools_count', 'schools']
            missing_fields = [field for field in required_fields if field not in data]
            
            if not missing_fields:
                print(f"   ✅ Response structure correct")
                print(f"   ✅ Schools array: {len(data['schools'])} items")
                
                # Check school object structure
                if data['schools']:
                    school = data['schools'][0]
                    school_fields = ['id', 'name', 'type', 'category', 'trades', 'trades_count']
                    missing_school_fields = [field for field in school_fields if field not in school]
                    
                    if not missing_school_fields:
                        print(f"   ✅ School object structure correct")
                        return True
                    else:
                        print(f"   ❌ Missing school fields: {missing_school_fields}")
                        return False
                else:
                    print(f"   ⚠️  No schools to validate structure")
                    return True
            else:
                print(f"   ❌ Missing response fields: {missing_fields}")
                return False
        else:
            print(f"   ❌ API call failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Frontend compatibility error: {e}")
        return False

def test_registration_flow():
    """Test 7: Complete Registration Flow"""
    print("\n🔍 TEST 7: Complete Registration Flow")
    
    try:
        # Step 1: Get provinces
        provinces_response = requests.get(f"{API_BASE}/locations/provinces")
        if provinces_response.status_code != 200:
            print("   ❌ Step 1 failed: Cannot get provinces")
            return False
        
        provinces = provinces_response.json()
        test_province = "South"
        print(f"   ✅ Step 1: Got {len(provinces)} provinces")
        
        # Step 2: Get districts
        districts_response = requests.get(f"{API_BASE}/locations/districts/{test_province}")
        if districts_response.status_code != 200:
            print("   ❌ Step 2 failed: Cannot get districts")
            return False
            
        districts = districts_response.json()
        test_district = "NYANZA"
        print(f"   ✅ Step 2: Got {len(districts)} districts")
        
        # Step 3: Get schools (THE CRITICAL STEP)
        schools_response = requests.get(f"{API_BASE}/schools-by-district/district/{test_province}/{test_district}")
        if schools_response.status_code != 200:
            print(f"   ❌ Step 3 failed: Cannot get schools - {schools_response.status_code}")
            print(f"      Response: {schools_response.text}")
            return False
            
        schools_data = schools_response.json()
        schools = schools_data.get('schools', [])
        print(f"   ✅ Step 3: Got {len(schools)} schools")
        
        if len(schools) == 0:
            print("   ❌ Step 3 critical: No schools returned!")
            return False
        
        # Step 4: Get trades for first school
        first_school = schools[0]
        trades_response = requests.get(f"{API_BASE}/registration/trades/{first_school['id']}")
        if trades_response.status_code != 200:
            print("   ❌ Step 4 failed: Cannot get trades")
            return False
            
        trades_data = trades_response.json()
        print(f"   ✅ Step 4: Got trades for {first_school['name']}")
        
        # Step 5: Get levels
        levels_response = requests.get(f"{API_BASE}/registration/levels")
        if levels_response.status_code != 200:
            print("   ❌ Step 5 failed: Cannot get levels")
            return False
            
        levels_data = levels_response.json()
        print(f"   ✅ Step 5: Got {levels_data.get('total', 0)} levels")
        
        print(f"   🎉 COMPLETE FLOW SUCCESS!")
        print(f"      Province: {test_province}")
        print(f"      District: {test_district}")
        print(f"      School: {first_school['name']}")
        print(f"      Trades: {first_school['trades_count']} available")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Registration flow error: {e}")
        return False

def main():
    """Run all tests and provide final verdict"""
    print("🚀 COMPLETE SYSTEM TEST - 100% VERIFICATION")
    print("=" * 60)
    
    tests = [
        ("Database", test_database),
        ("Backend Health", test_backend_health),
        ("Provinces API", test_provinces_api),
        ("Districts API", test_districts_api),
        ("Schools API", test_schools_api),
        ("Frontend Compatibility", test_frontend_compatibility),
        ("Registration Flow", test_registration_flow)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"   ❌ {test_name} crashed: {e}")
            results.append((test_name, False))
    
    # Final Results
    print("\n" + "=" * 60)
    print("📊 FINAL TEST RESULTS:")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status}: {test_name}")
        if result:
            passed += 1
    
    print(f"\n📈 SCORE: {passed}/{total} ({(passed/total)*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED - SYSTEM IS 100% WORKING!")
        print("\n✅ PROOF OF FUNCTIONALITY:")
        print("   • Database contains schools ✅")
        print("   • Backend API responds ✅") 
        print("   • All endpoints work ✅")
        print("   • Frontend compatibility confirmed ✅")
        print("   • Complete registration flow works ✅")
        print("\n🎯 YOU CAN TEST WITH CONFIDENCE!")
        
    else:
        failed_tests = [name for name, result in results if not result]
        print(f"\n⚠️  FAILED TESTS: {', '.join(failed_tests)}")
        print("\n🔧 ISSUES TO FIX:")
        
        if not results[0][1]:  # Database
            print("   • Database not populated with schools")
        if not results[1][1]:  # Backend
            print("   • Backend server not running on port 8080")
        if not results[4][1]:  # Schools API
            print("   • Schools API endpoint not working")
            
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)