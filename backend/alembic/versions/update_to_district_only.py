"""update to district only structure

Revision ID: update_district_only
Revises: add_location_schools
Create Date: 2024-01-15 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = 'update_district_only'
down_revision = 'add_location_schools'
branch_labels = None
depends_on = None


def upgrade():
    # Remove sector column from schools table
    op.drop_index('ix_schools_sector', table_name='schools')
    op.drop_column('schools', 'sector')
    op.drop_column('schools', 'trades')
    
    # Remove sector column from users table
    op.drop_index('ix_users_sector', table_name='users')
    op.drop_column('users', 'sector')


def downgrade():
    # Add back sector columns
    op.add_column('users', sa.Column('sector', sa.String(), nullable=True))
    op.create_index('ix_users_sector', 'users', ['sector'], unique=False)
    
    op.add_column('schools', sa.Column('sector', sa.String(), nullable=True))
    op.add_column('schools', sa.Column('trades', sa.JSON(), nullable=True))
    op.create_index('ix_schools_sector', 'schools', ['sector'], unique=False)
