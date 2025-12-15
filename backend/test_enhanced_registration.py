#!/usr/bin/env python3
"""
Test Enhanced Registration API Endpoints
Tests the new schools-by-district endpoints for the registration flow
"""

import requests
import json
import sys

API_BASE = "http://localhost:8080/api/v1"

def test_schools_summary():
    """Test the schools summary endpoint"""
    print("🔍 Testing Schools Summary...")
    
    try:
        response = requests.get(f"{API_BASE}/schools-by-district/summary")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Summary loaded successfully:")
            print(f"   Total Schools: {data['total_schools']}")
            print(f"   Total Provinces: {data['total_provinces']}")
            print(f"   Total Districts: {data['total_districts']}")
            print(f"   Districts by Province: {data['districts_by_province']}")
            return True
        else:
            print(f"❌ Failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_all_schools_by_district():
    """Test getting all schools organized by district"""
    print("\n🔍 Testing All Schools by District...")
    
    try:
        response = requests.get(f"{API_BASE}/schools-by-district/all")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ All schools loaded successfully:")
            
            for province in data:
                print(f"\n📍 {province['province']} ({province['total_schools']} schools)")
                
                for district in province['districts'][:3]:  # Show first 3 districts
                    print(f"   🏛️  {district['district']}: {district['schools_count']} schools")
                    
                    for school in district['schools'][:2]:  # Show first 2 schools
                        print(f"      • {school['name']} ({school['type']}) - {school['trades_count']} trades")
                
                if len(province['districts']) > 3:
                    print(f"   ... and {len(province['districts']) - 3} more districts")
            
            return True
        else:
            print(f"❌ Failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_specific_district():
    """Test getting schools for a specific district"""
    print("\n🔍 Testing Specific District (Kigali city/GASABO)...")
    
    try:
        response = requests.get(f"{API_BASE}/schools-by-district/district/Kigali city/GASABO")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ District schools loaded successfully:")
            print(f"   District: {data['district']}, {data['province']}")
            print(f"   Schools Count: {data['schools_count']}")
            
            for school in data['schools']:
                print(f"   • {school['name']} ({school['type']})")
                print(f"     Category: {school['category']}")
                print(f"     Trades: {school['trades_count']} available")
                if school['trades']:
                    trades_preview = school['trades'][:3]
                    trades_text = ", ".join(trades_preview)
                    if len(school['trades']) > 3:
                        trades_text += f" (+{len(school['trades']) - 3} more)"
                    print(f"     → {trades_text}")
                print()
            
            return True
        else:
            print(f"❌ Failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_registration_flow():
    """Test the complete registration flow"""
    print("\n🔍 Testing Complete Registration Flow...")
    
    # Test provinces
    try:
        response = requests.get(f"{API_BASE}/locations/provinces")
        if response.status_code == 200:
            provinces = response.json()
            print(f"✅ Provinces loaded: {len(provinces)} provinces")
        else:
            print(f"❌ Provinces failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Provinces error: {e}")
        return False
    
    # Test districts for a province
    try:
        response = requests.get(f"{API_BASE}/locations/districts/South")
        if response.status_code == 200:
            districts = response.json()
            print(f"✅ Districts loaded: {len(districts)} districts in South")
        else:
            print(f"❌ Districts failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Districts error: {e}")
        return False
    
    # Test schools in district
    try:
        response = requests.get(f"{API_BASE}/schools-by-district/district/South/NYANZA")
        if response.status_code == 200:
            schools_data = response.json()
            print(f"✅ Schools loaded: {schools_data['schools_count']} schools in NYANZA")
            
            if schools_data['schools']:
                first_school = schools_data['schools'][0]
                school_id = first_school['id']
                
                # Test trades for school
                try:
                    response = requests.get(f"{API_BASE}/registration/trades/{school_id}")
                    if response.status_code == 200:
                        trades_data = response.json()
                        if trades_data['success']:
                            print(f"✅ Trades loaded: {trades_data['total']} trades for {trades_data['school_name']}")
                        else:
                            print(f"⚠️  No trades available for school {school_id}")
                    else:
                        print(f"❌ Trades failed: {response.status_code}")
                except Exception as e:
                    print(f"❌ Trades error: {e}")
                
                # Test levels
                try:
                    response = requests.get(f"{API_BASE}/registration/levels")
                    if response.status_code == 200:
                        levels_data = response.json()
                        if levels_data['success']:
                            print(f"✅ Levels loaded: {levels_data['total']} levels available")
                        else:
                            print(f"⚠️  No levels available")
                    else:
                        print(f"❌ Levels failed: {response.status_code}")
                except Exception as e:
                    print(f"❌ Levels error: {e}")
        else:
            print(f"❌ Schools failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Schools error: {e}")
        return False
    
    return True

def main():
    """Run all tests"""
    print("🚀 ENHANCED REGISTRATION API TESTS")
    print("=" * 50)
    
    tests = [
        test_schools_summary,
        test_all_schools_by_district,
        test_specific_district,
        test_registration_flow
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 TEST RESULTS:")
    print(f"   Passed: {passed}/{total}")
    print(f"   Success Rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("\n🎯 REGISTRATION FLOW READY:")
        print("   1. User selects Province → District")
        print("   2. System auto-displays all schools in that district")
        print("   3. User selects school → System shows trades")
        print("   4. User selects trade → System shows levels")
        print("   5. User selects level → Registration complete")
    else:
        print(f"\n⚠️  {total - passed} tests failed. Check server status.")
        sys.exit(1)

if __name__ == "__main__":
    main()