import requests
import time

API_URL = "https://rwanda-edu-platform.onrender.com/api/v1"

print("Waiting for deployment to complete (60 seconds)...")
time.sleep(60)

print("\nCalling reload endpoint...")
response = requests.post(f"{API_URL}/admin/schools/reload-from-excel")

if response.status_code == 200:
    data = response.json()
    print("\nSUCCESS!")
    print(f"Schools loaded: {data['schools_loaded']}")
    print(f"\nRUNDA TVET Verification:")
    if data['runda_tvet_verification']:
        runda = data['runda_tvet_verification']
        print(f"  ID: {runda['id']}")
        print(f"  Name: {runda['name']}")
        print(f"  District: {runda['district']}")
        print(f"  Trades Count: {runda['trades_count']}")
        print(f"  Trades: {runda['trades']}")
    else:
        print("  RUNDA TVET not found!")
else:
    print(f"\nERROR: {response.status_code}")
    print(response.text)
