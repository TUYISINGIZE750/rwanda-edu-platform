"""Create direct_messages table"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import engine, Base
from app.models.direct_message import DirectMessage

def create_dm_table():
    print("🚀 Creating direct_messages table...")
    try:
        # Create the table
        Base.metadata.create_all(bind=engine, tables=[DirectMessage.__table__])
        print("✅ direct_messages table created successfully!")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    create_dm_table()
