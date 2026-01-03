#!/usr/bin/env python3
from backend.app.core.database import SessionLocal
from backend.app.models.user import User, UserRole
from backend.app.core.security import get_password_hash

def create_test_admin():
    db = SessionLocal()
    
    # Check if test admin exists
    existing_admin = db.query(User).filter(User.email == "testadmin@test.com").first()
    if existing_admin:
        print("Test admin already exists")
        db.close()
        return
    
    # Create test admin
    admin_user = User(
        email="testadmin@test.com",
        hashed_password=get_password_hash("admin123"),
        full_name="Test Admin",
        role=UserRole.ADMIN,
        school_id=1,
        province="Kigali City",
        district="Gasabo",
        is_active=1
    )
    
    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)
    
    print(f"Created test admin: {admin_user.email}")
    print(f"Password: admin123")
    print(f"ID: {admin_user.id}")
    
    db.close()

if __name__ == "__main__":
    create_test_admin()