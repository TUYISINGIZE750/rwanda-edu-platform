import requests
import json

def test_platform():
    base_url = "https://rwanda-edu-platform.onrender.com"
    
    tests = [
        {"name": "Health Check", "endpoint": "/health"},
        {"name": "Provinces API", "endpoint": "/api/v1/locations/provinces"},
        {"name": "Auth Test", "endpoint": "/api/v1/auth/test"},
    ]
    
    print("Testing Rwanda Education Platform...")
    print("=" * 50)
    
    for test in tests:
        try:
            url = f"{base_url}{test['endpoint']}"
            response = requests.get(url, timeout=10)
            
            status = "PASS" if response.status_code == 200 else "FAIL"
            print(f"{status} {test['name']} - HTTP {response.status_code}")
            
            if response.status_code == 200 and test['endpoint'] == "/api/v1/locations/provinces":
                data = response.json()
                print(f"   Found {len(data)} provinces")
                
        except Exception as e:
            print(f"FAIL {test['name']} - {str(e)}")
    
    print("=" * 50)

if __name__ == "__main__":
    test_platform()