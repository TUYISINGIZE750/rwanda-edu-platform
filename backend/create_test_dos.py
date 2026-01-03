"""Create a simple test DOS admin"""
from app.core.database import SessionLocal
from app.models.user import User, UserRole
from app.core.security import get_password_hash

def create_test_dos():
    db = SessionLocal()
    
    try:
        # Delete existing test DOS if exists
        existing = db.query(User).filter_by(email="test@dos.rw").first()
        if existing:
            db.delete(existing)
            db.commit()
        
        # Create simple test DOS
        dos = User(
            email="test@dos.rw",
            hashed_password=get_password_hash("test123"),
            full_name="Test DOS",
            role=UserRole.ADMIN,
            school_id=120524,  # FOREVER TVET INSTITUTE (from Excel)
            province="Kigali",
            district="Gasabo",
            is_active=1
        )
        
        db.add(dos)
        db.commit()
        
        print("SUCCESS: TEST DOS CREATED!")
        print("=" * 40)
        print("Email: test@dos.rw")
        print("Password: test123")
        print("Province: Kigali")
        print("District: Gasabo")
        print("School ID: 120524 (FOREVER TVET INSTITUTE)")
        print("Also manages: 121106 (International Technical School of Kigali)")
        print("=" * 40)
        
    except Exception as e:
        print(f"ERROR: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_dos()