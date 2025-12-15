"""Fix resources table schema"""
from app.core.database import engine, Base
from app.models.resource import Resource
from sqlalchemy import text

# Drop old table
with engine.connect() as conn:
    conn.execute(text("DROP TABLE IF EXISTS resources"))
    conn.commit()

# Create new table with correct schema
Base.metadata.create_all(bind=engine, tables=[Resource.__table__])

print("Resources table recreated successfully!")
