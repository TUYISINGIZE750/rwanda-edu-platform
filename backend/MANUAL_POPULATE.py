"""
MANUAL DATABASE POPULATION SCRIPT
Run this if automatic seeding fails on Render
"""
import requests
import time

API_URL = "https://rwanda-edu-platform.onrender.com/api/v1"

print("=" * 60)
print("MANUAL DATABASE POPULATION")
print("=" * 60)

# Step 1: Check if server is up
print("\n1. Checking server status...")
try:
    response = requests.get(f"{API_URL}/health", timeout=10)
    print(f"   [OK] Server is UP: {response.json()}")
except Exception as e:
    print(f"   [ERROR] Server is DOWN: {e}")
    print("   Please wait for deployment to complete and try again.")
    exit(1)

# Step 2: Add missing columns
print("\n2. Adding missing columns...")
try:
    response = requests.post(f"{API_URL}/admin/schools/add-columns", timeout=30)
    if response.status_code == 200:
        print(f"   [OK] Columns added: {response.json()}")
    else:
        print(f"   [WARN] Response: {response.status_code} - {response.text}")
except Exception as e:
    print(f"   [WARN] Could not add columns: {e}")
    print("   Continuing anyway (columns might already exist)...")

# Step 3: Reload schools from Excel
print("\n3. Loading schools from Excel file...")
print("   This may take 10-15 seconds...")
try:
    response = requests.post(f"{API_URL}/admin/schools/reload-from-excel", timeout=60)
    if response.status_code == 200:
        data = response.json()
        print(f"   [SUCCESS]!")
        print(f"   Schools loaded: {data.get('schools_loaded', 'unknown')}")
        if 'runda_tvet_verification' in data and data['runda_tvet_verification']:
            runda = data['runda_tvet_verification']
            print(f"\n   RUNDA TVET Verification:")
            print(f"   - ID: {runda['id']}")
            print(f"   - Name: {runda['name']}")
            print(f"   - District: {runda['district']}")
            print(f"   - Trades: {runda['trades_count']} trades")
            print(f"   - List: {runda['trades']}")
    else:
        print(f"   [FAILED]: {response.status_code}")
        print(f"   Error: {response.text[:500]}")
        exit(1)
except Exception as e:
    print(f"   [FAILED]: {e}")
    exit(1)

# Step 4: Verify schools are loaded
print("\n4. Verifying schools in database...")
try:
    response = requests.get(f"{API_URL}/locations/schools/district/South/KAMONYI", timeout=10)
    schools = response.json()
    print(f"   Schools in South/KAMONYI: {len(schools)}")
    for school in schools:
        print(f"   - {school['name']}: {len(school.get('trades', []))} trades")
except Exception as e:
    print(f"   [WARN] Could not verify: {e}")

print("\n" + "=" * 60)
print("DONE! Schools should now be loaded.")
print("Refresh your admin page and try again.")
print("=" * 60)
