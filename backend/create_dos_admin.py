"""Create a DOS (Deputy in charge of studies) admin user"""
from app.core.database import SessionLocal
from app.models.user import User, UserRole
from app.core.security import get_password_hash

def create_dos():
    db = SessionLocal()
    
    try:
        # Check if DOS already exists
        existing = db.query(User).filter_by(email="dos@iprc.ac.rw").first()
        if existing:
            print("DOS admin already exists!")
            print(f"Email: dos@iprc.ac.rw")
            print("Use password reset if needed")
            return
        
        # Create DOS admin
        dos = User(
            email="dos@iprc.ac.rw",
            hashed_password=get_password_hash("dos123"),
            full_name="DOS Administrator",
            role=UserRole.ADMIN,
            school_id=63,  # Same school as existing users
            province="Kigali",
            district="Gasabo",
            is_active=1
        )
        
        db.add(dos)
        db.commit()
        
        print("[SUCCESS] DOS Admin created!")
        print("=" * 50)
        print("Email: dos@iprc.ac.rw")
        print("Password: dos123")
        print("Role: DOS/Admin")
        print("School ID: 63")
        print("=" * 50)
        
    except Exception as e:
        print(f"[ERROR] Failed to create DOS: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_dos()
