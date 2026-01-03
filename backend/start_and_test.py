import subprocess
import time
import requests
import threading
import sys

def start_server():
    """Start the FastAPI server"""
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "app.main:app", 
            "--host", "127.0.0.1", 
            "--port", "8000"
        ], check=True)
    except KeyboardInterrupt:
        print("Server stopped")

def test_server():
    """Test the server after a delay"""
    print("Waiting for server to start...")
    time.sleep(3)
    
    try:
        response = requests.get("http://127.0.0.1:8000/", timeout=5)
        print(f"Server is running! Status: {response.status_code}")
        
        # Test auth endpoint
        response = requests.get("http://127.0.0.1:8000/api/v1/auth/me", timeout=5)
        print(f"Auth endpoint test: {response.status_code}")
        
    except Exception as e:
        print(f"Server test failed: {e}")

if __name__ == "__main__":
    print("Starting server and running tests...")
    print("Press Ctrl+C to stop the server")
    
    # Start test in a separate thread
    test_thread = threading.Thread(target=test_server)
    test_thread.daemon = True
    test_thread.start()
    
    # Start server (this will block)
    start_server()