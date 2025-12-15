import sys
sys.path.append('.')

from app.database import SessionLocal
from app.models.user import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

db = SessionLocal()
try:
    # Check teacher
    teacher = db.query(User).filter(User.email == 'Elam@gmail.com').first()
    if teacher:
        print(f'✓ Teacher: {teacher.email} (ID={teacher.id}, School={teacher.school_id})')
        # Test password
        if pwd_context.verify('password123', teacher.hashed_password):
            print('  ✓ Password "password123" is CORRECT')
        else:
            print('  ✗ Password "password123" is WRONG')
    else:
        print('✗ Teacher Elam@gmail.com NOT FOUND')
    
    print()
    
    # Check test students
    for i in range(1, 4):
        email = f'teststudent{i}@school.rw'
        student = db.query(User).filter(User.email == email).first()
        if student:
            print(f'✓ Student {i}: {student.email} (ID={student.id}, School={student.school_id})')
            if pwd_context.verify('password123', student.hashed_password):
                print(f'  ✓ Password "password123" is CORRECT')
            else:
                print(f'  ✗ Password "password123" is WRONG')
        else:
            print(f'✗ Student {email} NOT FOUND')
    
    print('\n--- All test users in database ---')
    test_users = db.query(User).filter(User.email.like('%test%')).all()
    for u in test_users:
        print(f'ID={u.id}, Email={u.email}, Name={u.first_name} {u.last_name}, Role={u.role}, School={u.school_id}')
        
finally:
    db.close()
