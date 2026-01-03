"""Check RUNDA TVET DOS credentials"""
from app.core.database import SessionLocal
from app.models.user import User
from app.core.security import verify_password

def check_dos():
    db = SessionLocal()
    
    try:
        # Check for RUNDA DOS user
        email = "dos.rundatvet.kamonyi@iprc.ac.rw"
        user = db.query(User).filter_by(email=email).first()
        
        if user:
            print(f"[OK] User found: {user.email}")
            print(f"  ID: {user.id}")
            print(f"  Name: {user.full_name}")
            print(f"  Role: {user.role}")
            print(f"  School ID: {user.school_id}")
            print(f"  Active: {user.is_active}")
            
            # Test password
            if verify_password("dos123", user.hashed_password):
                print("[OK] Password 'dos123' is correct")
            else:
                print("[ERROR] Password 'dos123' is incorrect")
                
        else:
            print(f"[ERROR] User {email} NOT FOUND")
            
            # Check all DOS users
            print("\nAll DOS users:")
            dos_users = db.query(User).filter(User.email.like('%dos%')).all()
            for u in dos_users:
                print(f"  {u.email} - {u.full_name} - School {u.school_id}")
                
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_dos()