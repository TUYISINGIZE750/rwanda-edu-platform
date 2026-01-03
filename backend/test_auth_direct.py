import requests
import socket

def test_auth_direct():
    # Try multiple possible URLs
    possible_urls = [
        "https://rwanda-edu-platform.onrender.com",
        "http://localhost:8000",
        "http://127.0.0.1:8000"
    ]
    
    working_url = None
    
    # Test each URL to find a working one
    for base_url in possible_urls:
        print(f"\nTesting connection to: {base_url}")
        try:
            # Test basic connectivity
            response = requests.get(f"{base_url}/", timeout=5)
            print(f"Connection successful! Status: {response.status_code}")
            working_url = base_url
            break
        except requests.exceptions.ConnectionError as e:
            if "getaddrinfo failed" in str(e):
                print("DNS resolution failed - domain may not exist")
            else:
                print(f"Connection refused - server may be down")
        except requests.exceptions.Timeout:
            print("Connection timeout")
        except Exception as e:
            print(f"Error: {e}")
    
    if not working_url:
        print("\n[ERROR] No working server found!")
        print("\nPossible solutions:")
        print("1. Check if the Render deployment is active")
        print("2. Start local server with: python -m uvicorn app.main:app --reload")
        print("3. Verify the correct domain name")
        return
    
    print(f"\n[SUCCESS] Using server: {working_url}")
    
    # Test auth endpoints
    try:
        print("\nTesting auth/me endpoint (should return 401/403)...")
        response = requests.get(f"{working_url}/api/v1/auth/me", timeout=10)
        print(f"Auth /me Response: {response.status_code}")
        if response.status_code in [401, 403]:
            print("[OK] Auth endpoint working (correctly returns 401/403 without token)")
        else:
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error testing /me endpoint: {e}")
    
    # Test login endpoint
    try:
        print("\nTesting login endpoint with invalid credentials...")
        login_data = {
            "email": "test@example.com",
            "password": "wrongpassword"
        }
        response = requests.post(f"{working_url}/api/v1/auth/login", json=login_data, timeout=10)
        print(f"Login Response: {response.status_code}")
        if response.status_code == 401:
            print("[OK] Login endpoint working (correctly rejects invalid credentials)")
        elif response.status_code == 422:
            print("[OK] Login endpoint working (validation error for invalid format)")
        else:
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error testing login endpoint: {e}")

if __name__ == "__main__":
    test_auth_direct()