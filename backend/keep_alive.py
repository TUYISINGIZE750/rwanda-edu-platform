import requests
import time
import os
from datetime import datetime

BACKEND_URL = os.getenv('BACKEND_URL', 'https://your-backend-url.com')
PING_INTERVAL = 600  # 10 minutes in seconds

def ping_backend():
    try:
        response = requests.get(f"{BACKEND_URL}/api/health", timeout=10)
        status = "✓ UP" if response.status_code == 200 else f"✗ DOWN ({response.status_code})"
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Backend {status}")
        return True
    except Exception as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Backend ✗ ERROR: {str(e)}")
        return False

if __name__ == "__main__":
    print(f"Keep-alive service started. Pinging {BACKEND_URL} every {PING_INTERVAL//60} minutes...")
    while True:
        ping_backend()
        time.sleep(PING_INTERVAL)
