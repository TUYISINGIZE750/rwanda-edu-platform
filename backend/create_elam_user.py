#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Create Elam user for testing"""

from app.core.database import SessionLocal
from app.models.user import User, UserRole
from app.core.security import get_password_hash

def create_elam_user():
    db = SessionLocal()
    
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == "Elam@gmail.com").first()
    if existing_user:
        print("User Elam@gmail.com already exists!")
        return
    
    # Create the user
    user = User(
        email="Elam@gmail.com",
        hashed_password=get_password_hash("teacher123"),  # Use same password as other teachers
        full_name="HAKIZIMANA Elam",
        role=UserRole.TEACHER,
        school_id=1,  # Assign to first school
        locale="en"
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    print("User created successfully!")
    print(f"Email: Elam@gmail.com")
    print(f"Password: teacher123")
    print(f"Role: {user.role.value}")
    print(f"School ID: {user.school_id}")
    
    db.close()

if __name__ == "__main__":
    create_elam_user()