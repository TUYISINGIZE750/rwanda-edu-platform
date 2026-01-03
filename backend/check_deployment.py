import requests
import time

# Trigger Render deployment
print("Checking Render service status...")

# Test if the fix is deployed
api_url = "https://rwanda-edu-platform.onrender.com/api/v1/locations/schools/district/Kigali%20city/Gasabo"
response = requests.get(api_url)

print(f"API Status: {response.status_code}")
print(f"Schools returned: {len(response.json())}")

if len(response.json()) == 0:
    print("\n❌ Fix NOT deployed yet!")
    print("\nMANUAL STEPS NEEDED:")
    print("1. Go to: https://dashboard.render.com")
    print("2. Click: rwanda-edu-backend")
    print("3. Click: Manual Deploy > Deploy latest commit")
    print("4. Wait 2-3 minutes")
else:
    print("\n✓ Fix is deployed!")
