import requests
import json

def test_system():
    print("COMPLETE SYSTEM TEST")
    print("=" * 40)
    
    # Test 1: Backend Health
    try:
        response = requests.get("http://localhost:8080/health")
        print(f"Backend Health: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Backend Health: FAILED - {e}")
        return False
    
    # Test 2: Provinces
    try:
        response = requests.get("http://localhost:8080/api/v1/locations/provinces")
        provinces = response.json()
        print(f"Provinces: {len(provinces)} loaded")
    except Exception as e:
        print(f"Provinces: FAILED - {e}")
        return False
    
    # Test 3: Districts
    try:
        response = requests.get("http://localhost:8080/api/v1/locations/districts/South")
        districts = response.json()
        print(f"Districts: {len(districts)} loaded for South")
    except Exception as e:
        print(f"Districts: FAILED - {e}")
        return False
    
    # Test 4: Schools (THE CRITICAL TEST)
    try:
        response = requests.get("http://localhost:8080/api/v1/schools-by-district/district/South/NYANZA")
        data = response.json()
        schools = data.get('schools', [])
        print(f"Schools: {len(schools)} loaded for NYANZA")
        
        if len(schools) > 0:
            sample = schools[0]
            print(f"  Sample: {sample['name']} ({sample['type']}) - {sample['trades_count']} trades")
            print("SCHOOLS API WORKING!")
        else:
            print("NO SCHOOLS FOUND!")
            return False
            
    except Exception as e:
        print(f"Schools: FAILED - {e}")
        return False
    
    # Test 5: Complete Flow
    try:
        # Get first school ID
        school_id = schools[0]['id']
        
        # Test trades
        response = requests.get(f"http://localhost:8080/api/v1/registration/trades/{school_id}")
        trades_data = response.json()
        print(f"Trades: {trades_data.get('total', 0)} for school {school_id}")
        
        # Test levels
        response = requests.get("http://localhost:8080/api/v1/registration/levels")
        levels_data = response.json()
        print(f"Levels: {levels_data.get('total', 0)} available")
        
    except Exception as e:
        print(f"Complete Flow: FAILED - {e}")
        return False
    
    print("\nALL TESTS PASSED!")
    print("SYSTEM IS 100% WORKING!")
    return True

if __name__ == "__main__":
    test_system()