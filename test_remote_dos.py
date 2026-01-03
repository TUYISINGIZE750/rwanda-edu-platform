#!/usr/bin/env python3
"""
Test DOS credentials on remote deployment
"""
import requests
import json

# Remote backend URL (update with your actual Render URL)
REMOTE_URL = "https://rwanda-edu-backend.onrender.com"

dos_credentials = {
    "email": "dos@iprc.ac.rw",
    "password": "dos123"
}

print("Testing DOS Admin Credentials on Remote Server...")
print("=" * 60)
print(f"Remote URL: {REMOTE_URL}")
print(f"Email: {dos_credentials['email']}")
print(f"Password: {dos_credentials['password']}")
print()

# Test login
print("1. Testing remote login...")
try:
    response = requests.post(
        f"{REMOTE_URL}/api/v1/auth/login",
        headers={"Content-Type": "application/json"},
        json=dos_credentials,
        timeout=30
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("REMOTE LOGIN SUCCESSFUL!")
        print(f"   User ID: {data.get('user', {}).get('id')}")
        print(f"   Full Name: {data.get('user', {}).get('full_name')}")
        print(f"   Role: {data.get('user', {}).get('role')}")
        print(f"   School ID: {data.get('user', {}).get('school_id')}")
        print(f"   Email: {data.get('user', {}).get('email')}")
        
        token = data.get('access_token')
        if token:
            print(f"   Token: {token[:20]}...")
            
            # Test DOS dashboard access
            print("\n2. Testing remote DOS Dashboard Access...")
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            dashboard_response = requests.get(
                f"{REMOTE_URL}/api/v1/dos/dashboard",
                headers=headers,
                timeout=30
            )
            
            print(f"Dashboard Status: {dashboard_response.status_code}")
            
            if dashboard_response.status_code == 200:
                dashboard_data = dashboard_response.json()
                print("REMOTE DOS DASHBOARD ACCESS SUCCESSFUL!")
                print("   Dashboard Stats:")
                stats = dashboard_data.get('stats', {})
                print(f"     - Total Teachers: {stats.get('total_teachers', 0)}")
                print(f"     - Total Students: {stats.get('total_students', 0)}")
                print(f"     - Total Classes: {stats.get('total_classes', 0)}")
                print(f"     - Class Teachers: {stats.get('class_teachers', 0)}")
                
                recent_teachers = dashboard_data.get('recent_teachers', [])
                print(f"     - Recent Teachers: {len(recent_teachers)}")
                
            else:
                print("REMOTE DOS DASHBOARD ACCESS FAILED!")
                print(f"   Error: {dashboard_response.text}")
        
    else:
        print("REMOTE LOGIN FAILED!")
        print(f"   Error: {response.text}")
        
except requests.exceptions.ConnectionError:
    print("CONNECTION ERROR!")
    print(f"   Cannot connect to remote server: {REMOTE_URL}")
    print("   Server may be starting up or deployment in progress...")
    
except Exception as e:
    print(f"ERROR: {e}")

print("\n" + "=" * 60)
print("REMOTE DEPLOYMENT STATUS:")
print("- If login successful: DOS admin system is working remotely")
print("- If connection error: Wait for deployment to complete")
print("- Frontend should be accessible at your Cloudflare/Netlify URL")