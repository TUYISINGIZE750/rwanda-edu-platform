"""Add school fields for TVET data

Revision ID: add_school_fields
Revises: update_to_district_only
Create Date: 2024-01-01 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_school_fields'
down_revision = '546f25b246e8'
branch_labels = None
depends_on = None

def upgrade():
    # Add new columns to schools table
    op.add_column('schools', sa.Column('school_code', sa.String(), nullable=True))
    op.add_column('schools', sa.Column('trades_full', sa.String(), nullable=True))
    op.add_column('schools', sa.Column('trades_short', sa.String(), nullable=True))
    op.add_column('schools', sa.Column('gender', sa.String(), nullable=True))
    
    # Create index on school_code
    op.create_index('ix_schools_school_code', 'schools', ['school_code'])
    
    # Drop old trades column if it exists
    try:
        op.drop_column('schools', 'trades')
    except:
        pass  # Column might not exist

def downgrade():
    # Remove new columns
    op.drop_index('ix_schools_school_code', 'schools')
    op.drop_column('schools', 'school_code')
    op.drop_column('schools', 'trades_full')
    op.drop_column('schools', 'trades_short')
    op.drop_column('schools', 'gender')
    
    # Add back old trades column
    op.add_column('schools', sa.Column('trades', sa.String(), nullable=True))