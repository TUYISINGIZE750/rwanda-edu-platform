import requests

API_URL = "https://rwanda-edu-platform.onrender.com"

print("Testing API endpoint...")
r = requests.get(f"{API_URL}/api/v1/locations/schools/district/Kigali%20city/Gasabo")
print(f"Status: {r.status_code}")
print(f"Response: {r.text}")
