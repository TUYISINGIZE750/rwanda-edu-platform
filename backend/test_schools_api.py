import requests

API_URL = "https://rwanda-edu-platform.onrender.com"

# Test 1: Get provinces
print("1. Testing provinces...")
r = requests.get(f"{API_URL}/api/v1/locations/provinces")
print(f"Status: {r.status_code}")
print(f"Provinces: {r.json()}\n")

# Test 2: Get districts for South
print("2. Testing districts for South...")
r = requests.get(f"{API_URL}/api/v1/locations/districts/South")
print(f"Status: {r.status_code}")
print(f"Districts: {r.json()}\n")

# Test 3: Get schools for South/Kamonyi
print("3. Testing schools for South/Kamonyi...")
r = requests.get(f"{API_URL}/api/v1/locations/schools/district/South/Kamonyi")
print(f"Status: {r.status_code}")
print(f"Schools: {r.json()}")
