import requests
import json

BASE_URL = "http://localhost:8080"

def test_login():
    # Test login with created user
    login_data = {
        "email": "student@test.com",
        "password": "test123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/v1/auth/login", json=login_data)
        print(f"Login Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("Login successful!")
            print(f"User: {data['user']['full_name']} ({data['user']['role']})")
            print(f"Token: {data['access_token'][:50]}...")
            return True
        else:
            print(f"Login failed: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("Cannot connect to backend server.")
        print("Make sure the backend is running on port 8080")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_all_users():
    users = [
        ("student@test.com", "student"),
        ("teacher@test.com", "teacher"), 
        ("admin@test.com", "admin")
    ]
    
    for email, role in users:
        print(f"\nTesting {role} login...")
        login_data = {"email": email, "password": "test123"}
        
        try:
            response = requests.post(f"{BASE_URL}/api/v1/auth/login", json=login_data)
            if response.status_code == 200:
                data = response.json()
                print(f"✓ {role} login successful: {data['user']['full_name']}")
            else:
                print(f"✗ {role} login failed: {response.status_code}")
        except Exception as e:
            print(f"✗ {role} login error: {e}")

if __name__ == "__main__":
    print("Testing login functionality...")
    test_all_users()