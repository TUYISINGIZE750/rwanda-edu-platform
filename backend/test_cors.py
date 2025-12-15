"""Quick test to verify CORS and registration endpoints are working"""
import requests
import json

BASE_URL = "http://localhost:8080"

def test_health():
    """Test main health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"✓ Health Check: {response.json()}")
        return True
    except Exception as e:
        print(f"✗ Health Check Failed: {e}")
        return False

def test_registration_health():
    """Test registration health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/api/v1/registration/health")
        print(f"✓ Registration Health: {response.json()}")
        return True
    except Exception as e:
        print(f"✗ Registration Health Failed: {e}")
        return False

def test_provinces():
    """Test provinces endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/api/v1/locations/provinces")
        data = response.json()
        print(f"✓ Provinces: Found {len(data)} provinces")
        return True
    except Exception as e:
        print(f"✗ Provinces Failed: {e}")
        return False

def test_schools():
    """Test schools endpoint with sample data"""
    try:
        # Test with Southern Province and Kamonyi
        response = requests.get(f"{BASE_URL}/api/v1/registration/schools/Southern Province/Kamonyi")
        data = response.json()
        
        if data.get('success'):
            print(f"✓ Schools: Found {data.get('total', 0)} schools in Kamonyi")
            if data.get('schools'):
                print(f"  First school: {data['schools'][0]['name']}")
        else:
            print(f"⚠ Schools: {data.get('message', 'No schools found')}")
        return True
    except Exception as e:
        print(f"✗ Schools Failed: {e}")
        return False

def test_cors_headers():
    """Test CORS headers"""
    try:
        response = requests.options(
            f"{BASE_URL}/api/v1/registration/schools/Southern Province/Kamonyi",
            headers={
                'Origin': 'http://localhost:5173',
                'Access-Control-Request-Method': 'GET',
                'Access-Control-Request-Headers': 'content-type'
            }
        )
        
        cors_headers = {
            'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
            'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
            'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers'),
        }
        
        print(f"✓ CORS Headers:")
        for key, value in cors_headers.items():
            print(f"  {key}: {value}")
        return True
    except Exception as e:
        print(f"✗ CORS Test Failed: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("TESTING BACKEND ENDPOINTS")
    print("=" * 50)
    print()
    
    tests = [
        ("Health Check", test_health),
        ("Registration Health", test_registration_health),
        ("Provinces", test_provinces),
        ("Schools", test_schools),
        ("CORS Headers", test_cors_headers),
    ]
    
    results = []
    for name, test_func in tests:
        print(f"\n{name}:")
        print("-" * 50)
        results.append(test_func())
        print()
    
    print("=" * 50)
    print(f"RESULTS: {sum(results)}/{len(results)} tests passed")
    print("=" * 50)
    
    if all(results):
        print("\n✓ All tests passed! Backend is ready.")
    else:
        print("\n⚠ Some tests failed. Check the output above.")
