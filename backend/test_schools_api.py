"""Test script to verify schools API endpoints work correctly"""
import requests
import json

BASE_URL = "http://localhost:8080/api/v1"

def test_schools_by_district():
    """Test the schools-by-district endpoint"""
    
    # Test case: South province, KAMONYI district
    province = "South"
    district = "KAMONYI"
    
    url = f"{BASE_URL}/schools-by-district/district/{province}/{district}"
    print(f"\nTesting: {url}")
    
    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\nDistrict: {data['district']}")
            print(f"Province: {data['province']}")
            print(f"Schools Count: {data['schools_count']}")
            print(f"\nSchools:")
            for school in data['schools']:
                print(f"  - {school['name']} ({school['type']})")
                print(f"    Trades: {', '.join(school['trades'][:3])}...")
        else:
            print(f"Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("ERROR: Cannot connect to backend. Make sure it's running on port 8080")
    except Exception as e:
        print(f"ERROR: {e}")

def test_locations_endpoint():
    """Test the locations endpoint"""
    
    province = "South"
    district = "KAMONYI"
    
    url = f"{BASE_URL}/locations/schools/district/Southern%20Province/{district}"
    print(f"\nTesting locations endpoint: {url}")
    
    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Found {len(data)} schools")
            for school in data[:2]:
                print(f"  - {school['name']}")
        else:
            print(f"Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("ERROR: Cannot connect to backend")
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("TESTING SCHOOLS API ENDPOINTS")
    print("=" * 60)
    
    test_schools_by_district()
    test_locations_endpoint()
    
    print("\n" + "=" * 60)
    print("TESTS COMPLETE")
    print("=" * 60)
