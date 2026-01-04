"""add can_create_groups permission

Revision ID: add_can_create_groups
Revises: 
Create Date: 2024-01-20

"""
from alembic import op
import sqlalchemy as sa

revision = 'add_can_create_groups'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Add can_create_groups column
    op.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS can_create_groups INTEGER DEFAULT 0")
    
    # Auto-grant permission to existing class teachers
    op.execute("UPDATE users SET can_create_groups = 1 WHERE is_class_teacher = 1")

def downgrade():
    op.execute("ALTER TABLE users DROP COLUMN IF EXISTS can_create_groups")
