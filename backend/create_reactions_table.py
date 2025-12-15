from sqlalchemy import text
from app.core.database import engine

try:
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS reactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                emoji VARCHAR(10) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (message_id) REFERENCES messages(id),
                FOREIGN KEY (user_id) REFERENCES users(id),
                UNIQUE(message_id, user_id, emoji)
            );
        """))
        conn.commit()
        print("SUCCESS: reactions table created")
except Exception as e:
    print(f"ERROR: {e}")
