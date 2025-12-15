import requests
import json

# Test backend endpoints
BASE_URL = "http://localhost:8080"

def test_health():
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Health check: {response.status_code} - {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_auth_endpoints():
    try:
        # Test login endpoint
        login_data = {"email": "test@example.com", "password": "test123"}
        response = requests.post(f"{BASE_URL}/api/v1/auth/login", json=login_data)
        print(f"Login endpoint: {response.status_code}")
        
        # Test register endpoint  
        register_data = {
            "email": "newuser@example.com",
            "password": "test123",
            "full_name": "Test User",
            "role": "student",
            "school_id": 1,
            "province": "Kigali City",
            "district": "Gasabo",
            "locale": "en"
        }
        response = requests.post(f"{BASE_URL}/api/v1/auth/register", json=register_data)
        print(f"Register endpoint: {response.status_code}")
        
    except Exception as e:
        print(f"Auth endpoints test failed: {e}")

def test_groups_endpoint():
    try:
        response = requests.get(f"{BASE_URL}/api/v1/directory/groups")
        print(f"Groups endpoint: {response.status_code}")
    except Exception as e:
        print(f"Groups endpoint test failed: {e}")

if __name__ == "__main__":
    print("Testing backend endpoints...")
    
    if test_health():
        print("Backend is running")
        test_auth_endpoints()
        test_groups_endpoint()
    else:
        print("Backend is not running or not accessible")
        print("Make sure to start the backend server on port 8080")