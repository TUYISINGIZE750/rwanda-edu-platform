#!/usr/bin/env python3
"""
Test DOS credentials on correct remote URL
"""
import requests

# Correct remote URL based on deployment files
REMOTE_URL = "https://rwanda-edu-platform.onrender.com"

dos_credentials = {
    "email": "dos@iprc.ac.rw",
    "password": "dos123"
}

print("Testing DOS Admin on Correct Remote URL...")
print("=" * 60)
print(f"Remote URL: {REMOTE_URL}")
print()

# Test server health first
print("1. Testing server health...")
try:
    response = requests.get(f"{REMOTE_URL}/", timeout=30)
    print(f"Root Status: {response.status_code}")
    if response.status_code == 200:
        print("Server is UP!")
    else:
        print(f"Server response: {response.text[:200]}")
except Exception as e:
    print(f"Server connection error: {e}")

print()

# Test DOS login
print("2. Testing DOS login...")
try:
    response = requests.post(
        f"{REMOTE_URL}/api/v1/auth/login",
        headers={"Content-Type": "application/json"},
        json=dos_credentials,
        timeout=30
    )
    
    print(f"Login Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("✅ REMOTE DOS LOGIN SUCCESSFUL!")
        print(f"   User: {data.get('user', {}).get('full_name')}")
        print(f"   Role: {data.get('user', {}).get('role')}")
        print(f"   School: {data.get('user', {}).get('school_id')}")
        
        token = data.get('access_token')
        if token:
            # Test dashboard
            print("\n3. Testing DOS Dashboard...")
            headers = {"Authorization": f"Bearer {token}"}
            
            dashboard_response = requests.get(
                f"{REMOTE_URL}/api/v1/dos/dashboard",
                headers=headers,
                timeout=30
            )
            
            if dashboard_response.status_code == 200:
                dashboard_data = dashboard_response.json()
                print("✅ DOS DASHBOARD WORKING!")
                stats = dashboard_data.get('stats', {})
                print(f"   Teachers: {stats.get('total_teachers', 0)}")
                print(f"   Students: {stats.get('total_students', 0)}")
                print(f"   Classes: {stats.get('total_classes', 0)}")
            else:
                print(f"❌ Dashboard failed: {dashboard_response.status_code}")
        
    else:
        print(f"❌ Login failed: {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"❌ Login error: {e}")

print("\n" + "=" * 60)
print("DEPLOYMENT STATUS:")
print("✅ Code pushed to GitHub")
print("⏳ Render deployment may take 2-5 minutes")
print("🔗 Check deployment at: https://dashboard.render.com")
print("📱 Frontend URL: Check your Cloudflare/Netlify deployment")