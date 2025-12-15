import uvicorn
import sys
import os

# Add the backend directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

if __name__ == "__main__":
    print("Starting Rwanda TVET Platform Backend...")
    print("Server will be available at: http://localhost:8080")
    print("API documentation at: http://localhost:8080/docs")
    print("\nTest users available:")
    print("Student: student@test.com / test123")
    print("Teacher: teacher@test.com / test123")
    print("Admin: admin@test.com / test123")
    print("\nPress Ctrl+C to stop the server")
    
    try:
        uvicorn.run(
            "backend.app.main:app",
            host="0.0.0.0",
            port=8080,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\nServer stopped.")
    except Exception as e:
        print(f"Error starting server: {e}")
        print("Make sure you have installed all dependencies:")
        print("pip install fastapi uvicorn sqlalchemy pydantic bcrypt python-jose")