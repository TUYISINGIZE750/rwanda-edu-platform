"""Fix RUNDA TVET DOS password"""
from app.core.database import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash

def fix_dos_password():
    db = SessionLocal()
    
    try:
        email = "dos.rundatvet.kamonyi@iprc.ac.rw"
        user = db.query(User).filter_by(email=email).first()
        
        if user:
            # Update password to dos123
            user.hashed_password = get_password_hash("dos123")
            db.commit()
            
            print(f"[SUCCESS] Password updated for {email}")
            print("New password: dos123")
        else:
            print(f"[ERROR] User {email} not found")
            
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_dos_password()