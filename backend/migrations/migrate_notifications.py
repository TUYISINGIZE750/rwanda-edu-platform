"""
Database Migration: Add Notifications Table
Run this with your production DATABASE_URL
"""

from sqlalchemy import create_engine, text
import os
import sys

def run_migration():
    # Get DATABASE_URL from environment or ask user
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        print("\nWARNING: DATABASE_URL not found in environment variables")
        print("\nPlease enter your production database URL:")
        print("(Format: postgresql://user:password@host:port/database)")
        database_url = input("\nDATABASE_URL: ").strip()
        
        if not database_url:
            print("ERROR: No database URL provided. Exiting.")
            sys.exit(1)
    
    # Fix Render's postgres:// to postgresql://
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    
    print("\nConnecting to database...")
    
    try:
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            # Create notifications table
            print("Creating notifications table...")
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS notifications (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    type VARCHAR(50) NOT NULL,
                    title VARCHAR(255) NOT NULL,
                    message TEXT NOT NULL,
                    link VARCHAR(500),
                    is_read BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    related_id INTEGER,
                    related_type VARCHAR(50)
                );
            """))
            
            # Create indexes
            print("Creating indexes...")
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_notifications_user_id ON notifications(user_id);
            """))
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_notifications_is_read ON notifications(is_read);
            """))
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_notifications_created_at ON notifications(created_at DESC);
            """))
            
            conn.commit()
            print("\nSUCCESS: Notifications table created!")
            print("SUCCESS: Indexes created!")
            print("\nMigration completed! Your notification system is ready.")
            
    except Exception as e:
        print(f"\nERROR: Migration failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("=" * 60)
    print("  TSSANYWHERE - Notifications Table Migration")
    print("=" * 60)
    run_migration()
