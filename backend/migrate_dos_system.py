"""Migration script to add DOS system fields"""
from app.core.database import SessionLocal, engine
from sqlalchemy import text

def migrate():
    db = SessionLocal()
    
    try:
        print("Adding new fields to users table...")
        
        # Add new fields to users table (SQLite doesn't support IF NOT EXISTS)
        try:
            db.execute(text("ALTER TABLE users ADD COLUMN is_class_teacher INTEGER DEFAULT 0"))
            print("  Added is_class_teacher column")
        except:
            print("  is_class_teacher column already exists")
        
        try:
            db.execute(text("ALTER TABLE users ADD COLUMN managed_class_id INTEGER"))
            print("  Added managed_class_id column")
        except:
            print("  managed_class_id column already exists")
        
        try:
            db.execute(text("ALTER TABLE users ADD COLUMN generated_password VARCHAR(255)"))
            print("  Added generated_password column")
        except:
            print("  generated_password column already exists")
        
        db.commit()
        print("[OK] Users table updated")
        
        # Create teacher_class_access table
        print("Creating teacher_class_access table...")
        db.execute(text("""
            CREATE TABLE IF NOT EXISTS teacher_class_access (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                teacher_id INTEGER NOT NULL,
                group_id INTEGER NOT NULL,
                granted_by INTEGER NOT NULL,
                module_name VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))
        
        db.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_teacher_class_access_teacher 
            ON teacher_class_access(teacher_id)
        """))
        
        db.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_teacher_class_access_group 
            ON teacher_class_access(group_id)
        """))
        
        db.commit()
        print("[OK] teacher_class_access table created")
        
        print("\n[SUCCESS] Migration completed successfully!")
        
    except Exception as e:
        print(f"[ERROR] Migration failed: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    migrate()
