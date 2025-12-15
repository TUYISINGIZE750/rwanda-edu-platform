"""Create database directly without migrations"""
from app.core.database import Base, engine
from app.models.user import User
from app.models.school import School

print("Creating all tables...")
Base.metadata.create_all(engine)
print("✓ Database created successfully!")
