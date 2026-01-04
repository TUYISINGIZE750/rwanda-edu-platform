"""
WAIT FOR DEPLOYMENT AND POPULATE DATABASE
This script waits for Render to finish deploying, then populates the database
"""
import requests
import time

API_URL = "https://rwanda-edu-platform.onrender.com/api/v1"

print("="*60)
print("WAITING FOR DEPLOYMENT TO COMPLETE...")
print("="*60)

# Wait for deployment (check every 30 seconds for 5 minutes)
max_attempts = 10
attempt = 0

while attempt < max_attempts:
    attempt += 1
    print(f"\nAttempt {attempt}/{max_attempts}: Checking if new code is deployed...")
    
    try:
        # Check if the new endpoint exists
        response = requests.post(f"{API_URL}/admin/schools/add-columns", timeout=10)
        if response.status_code != 404:
            print("[OK] New code is deployed!")
            break
        else:
            print("[WAIT] Still deploying... (endpoint returns 404)")
    except Exception as e:
        print(f"[WAIT] Server not ready: {e}")
    
    if attempt < max_attempts:
        print("Waiting 30 seconds before next check...")
        time.sleep(30)
else:
    print("\n[TIMEOUT] Deployment taking too long. Please check Render dashboard.")
    print("Then run MANUAL_POPULATE.py manually.")
    exit(1)

# Now run the population
print("\n" + "="*60)
print("RUNNING DATABASE POPULATION...")
print("="*60)

# Step 1: Add columns
print("\n1. Adding missing columns...")
try:
    response = requests.post(f"{API_URL}/admin/schools/add-columns", timeout=30)
    print(f"   Response: {response.status_code} - {response.text[:200]}")
except Exception as e:
    print(f"   Error: {e}")

# Step 2: Load schools
print("\n2. Loading schools from Excel...")
try:
    response = requests.post(f"{API_URL}/admin/schools/reload-from-excel", timeout=60)
    if response.status_code == 200:
        data = response.json()
        print(f"   [SUCCESS] Schools loaded: {data.get('schools_loaded', 'unknown')}")
        if 'runda_tvet_verification' in data:
            runda = data['runda_tvet_verification']
            if runda:
                print(f"   RUNDA TVET: {runda['trades_count']} trades - {runda['trades']}")
    else:
        print(f"   [FAILED] {response.status_code}: {response.text[:300]}")
except Exception as e:
    print(f"   [ERROR]: {e}")

print("\n" + "="*60)
print("DONE! Check https://tssanywhere.pages.dev/admin-login")
print("="*60)
