import requests

API_BASE = "http://localhost:8080/api/v1"

def test_api():
    try:
        # Test summary
        response = requests.get(f"{API_BASE}/schools-by-district/summary")
        print(f"Summary: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Total schools: {data['total_schools']}")
        
        # Test specific district
        response = requests.get(f"{API_BASE}/schools-by-district/district/South/NYANZA")
        print(f"NYANZA schools: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Schools in NYANZA: {data['schools_count']}")
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"Connection error: {e}")
        print("Make sure backend is running on port 8080")

if __name__ == "__main__":
    test_api()