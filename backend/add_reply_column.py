from sqlalchemy import text
from app.core.database import engine

try:
    with engine.connect() as conn:
        conn.execute(text("ALTER TABLE messages ADD COLUMN reply_to_id INTEGER REFERENCES messages(id);"))
        conn.commit()
        print("SUCCESS: reply_to_id column added to messages table")
except Exception as e:
    if "duplicate column" in str(e).lower() or "already exists" in str(e).lower():
        print("SUCCESS: reply_to_id column already exists")
    else:
        print(f"ERROR: {e}")
