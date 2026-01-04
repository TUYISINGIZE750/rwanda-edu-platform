"""
Database Migration: Add Notifications Table
Run this script to add the notifications table to your database
"""

from sqlalchemy import create_engine, text
import os

# Database URL from environment or default
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/tssanywhere")

def run_migration():
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as conn:
        # Create notifications table
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
        
        # Create indexes for better performance
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_notifications_user_id ON notifications(user_id);
            CREATE INDEX IF NOT EXISTS idx_notifications_is_read ON notifications(is_read);
            CREATE INDEX IF NOT EXISTS idx_notifications_created_at ON notifications(created_at DESC);
        """))
        
        conn.commit()
        print("✅ Notifications table created successfully!")

if __name__ == "__main__":
    run_migration()
