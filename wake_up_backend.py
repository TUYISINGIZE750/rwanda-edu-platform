import requests
import time

def wake_up_backend():
    """Wake up the Render backend by making requests to common endpoints"""
    backend_url = "https://rwanda-edu-platform.onrender.com"
    endpoints = ["/", "/api", "/api/v1", "/health"]
    
    print("🚀 Waking up Rwanda Education Platform backend...")
    
    for endpoint in endpoints:
        try:
            url = f"{backend_url}{endpoint}"
            print(f"📡 Pinging {url}...")
            response = requests.get(url, timeout=30)
            print(f"✅ Response: {response.status_code}")
            if response.status_code in [200, 404]:  # 404 is fine, means server is awake
                print("🎉 Backend is awake!")
                return True
        except Exception as e:
            print(f"⚠️  {endpoint}: {str(e)}")
            continue
    
    print("⏰ Backend is starting up, please wait...")
    return False

if __name__ == "__main__":
    wake_up_backend()