from .database import SessionLocal
from .models.user import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

db = SessionLocal()
try:
    # Check teacher
    teacher = db.query(User).filter(User.email == 'Elam@gmail.com').first()
    if teacher:
        print(f'✓ Teacher: {teacher.email} (ID={teacher.id}, School={teacher.school_id})')
        if pwd_context.verify('password123', teacher.hashed_password):
            print('  ✓ Password "password123" WORKS')
        else:
            print('  ✗ Password "password123" FAILS')
    else:
        print('✗ Teacher NOT FOUND')
    
    print()
    
    # Check test students
    for i in range(1, 4):
        email = f'teststudent{i}@school.rw'
        student = db.query(User).filter(User.email == email).first()
        if student:
            print(f'✓ Student {i}: {student.email} (ID={student.id})')
            if pwd_context.verify('password123', student.hashed_password):
                print(f'  ✓ Password WORKS')
            else:
                print(f'  ✗ Password FAILS')
        else:
            print(f'✗ Student {i} NOT FOUND')
        
finally:
    db.close()
