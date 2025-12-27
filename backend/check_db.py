"""Check database status"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

try:
    from app.core.database import SessionLocal, engine
    from app.models.school import School
    from sqlalchemy import inspect
    
    print("Connecting to database...")
    db = SessionLocal()
    
    # Check if table exists
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"Tables: {tables}")
    
    if 'schools' in tables:
        # Check columns
        columns = inspector.get_columns('schools')
        print(f"\nSchools table columns:")
        for col in columns:
            print(f"  - {col['name']}: {col['type']}")
        
        # Count schools
        count = db.query(School).count()
        print(f"\nTotal schools: {count}")
        
        if count > 0:
            # Show first school
            school = db.query(School).first()
            print(f"\nFirst school:")
            print(f"  Name: {school.name}")
            print(f"  District: {school.district}")
            print(f"  Province: {school.province}")
            print(f"  Trades: {school.trades}")
    else:
        print("Schools table does not exist!")
    
    db.close()
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
