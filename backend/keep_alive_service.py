"""
Keep-Alive Service - Prevents Render from going to sleep
Pings the server every 10 minutes
"""
import requests
import time
from datetime import datetime

API_URL = "https://rwanda-edu-platform.onrender.com"

def ping_server():
    try:
        response = requests.get(f"{API_URL}/health", timeout=10)
        if response.status_code == 200:
            print(f"[{datetime.now()}] ✓ Server alive")
            return True
    except Exception as e:
        print(f"[{datetime.now()}] ✗ Ping failed: {e}")
    return False

def keep_alive():
    print("Keep-Alive Service Started")
    print(f"Pinging: {API_URL}")
    print("="*50)
    
    while True:
        ping_server()
        time.sleep(600)  # 10 minutes

if __name__ == "__main__":
    keep_alive()
