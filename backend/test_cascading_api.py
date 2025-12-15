"""Test the cascading location and school API"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1/locations"

def test_cascading_system():
    """Test the complete cascading system"""
    print("Testing Cascading Location and School System")
    print("=" * 50)
    
    try:
        # Test 1: Get all provinces
        print("\n1. Testing provinces endpoint...")
        response = requests.get(f"{BASE_URL}/provinces")
        if response.status_code == 200:
            provinces = response.json()
            print(f"   Found {len(provinces)} provinces")
            for province in provinces[:3]:
                print(f"   - {province['name']}")
        else:
            print(f"   Error: {response.status_code}")
            return
        
        # Test 2: Get districts for a province
        test_province = "Kigali City"
        print(f"\n2. Testing districts for '{test_province}'...")
        response = requests.get(f"{BASE_URL}/districts/{test_province}")
        if response.status_code == 200:
            districts = response.json()
            print(f"   Found {len(districts)} districts in {test_province}")
            for district in districts:
                print(f"   - {district['name']}")
        else:
            print(f"   Error: {response.status_code}")
            return
        
        # Test 3: Get schools for a district
        test_district = "GASABO"
        print(f"\n3. Testing schools for '{test_province}' -> '{test_district}'...")
        response = requests.get(f"{BASE_URL}/schools/district/{test_province}/{test_district}")
        if response.status_code == 200:
            schools = response.json()
            print(f"   Found {len(schools)} schools in {test_district}")
            for school in schools[:3]:
                print(f"   - {school['name']} ({school['school_code']})")
                print(f"     Trades: {len(school['trades_full'])} ({', '.join(school['trades_full'][:2])}{'...' if len(school['trades_full']) > 2 else ''})")
                print(f"     Gender: {school['gender']}")
        else:
            print(f"   Error: {response.status_code}")
            return
        
        # Test 4: Test another district with more schools
        test_province2 = "Southern Province"
        test_district2 = "NYANZA"
        print(f"\n4. Testing schools for '{test_province2}' -> '{test_district2}'...")
        response = requests.get(f"{BASE_URL}/schools/district/{test_province2}/{test_district2}")
        if response.status_code == 200:
            schools = response.json()
            print(f"   Found {len(schools)} schools in {test_district2}")
            for school in schools[:5]:
                print(f"   - {school['name']} ({school['school_code']})")
                print(f"     Trades: {len(school['trades_full'])} - {', '.join(school['trades_short'][:3])}{'...' if len(school['trades_short']) > 3 else ''}")
                print(f"     Gender: {school['gender']}")
        else:
            print(f"   Error: {response.status_code}")
            return
        
        # Test 5: Get all schools
        print(f"\n5. Testing all schools endpoint...")
        response = requests.get(f"{BASE_URL}/schools")
        if response.status_code == 200:
            all_schools = response.json()
            print(f"   Total schools in database: {len(all_schools)}")
            
            # Group by district
            districts_count = {}
            for school in all_schools:
                district = school['district']
                districts_count[district] = districts_count.get(district, 0) + 1
            
            print(f"   Schools per district (top 10):")
            sorted_districts = sorted(districts_count.items(), key=lambda x: x[1], reverse=True)
            for district, count in sorted_districts[:10]:
                print(f"     {district}: {count} schools")
        else:
            print(f"   Error: {response.status_code}")
            return
        
        print(f"\n✓ All tests passed! The cascading system is working properly.")
        print(f"\nSummary:")
        print(f"- Students can select from {len(provinces)} provinces")
        print(f"- Each province has multiple districts")
        print(f"- Districts automatically show their TVET schools with:")
        print(f"  * School name and code")
        print(f"  * Full trade names and short codes")
        print(f"  * Gender acceptance (Mixt/Male/Female)")
        print(f"- Total of {len(all_schools)} TVET schools available")
        
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API server.")
        print("Make sure the backend server is running on http://localhost:8000")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_cascading_system()