"""add location fields and schools table

Revision ID: add_location_schools
Revises: 
Create Date: 2024-01-15 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'add_location_schools'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create schools table
    op.create_table('schools',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('type', sa.String(), nullable=False),
        sa.Column('category', sa.String(), nullable=False),
        sa.Column('province', sa.String(), nullable=False),
        sa.Column('district', sa.String(), nullable=False),
        sa.Column('sector', sa.String(), nullable=False),
        sa.Column('trades', sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_schools_id'), 'schools', ['id'], unique=False)
    op.create_index(op.f('ix_schools_name'), 'schools', ['name'], unique=False)
    op.create_index(op.f('ix_schools_province'), 'schools', ['province'], unique=False)
    op.create_index(op.f('ix_schools_district'), 'schools', ['district'], unique=False)
    op.create_index(op.f('ix_schools_sector'), 'schools', ['sector'], unique=False)
    
    # Add location columns to users table
    op.add_column('users', sa.Column('province', sa.String(), nullable=True))
    op.add_column('users', sa.Column('district', sa.String(), nullable=True))
    op.add_column('users', sa.Column('sector', sa.String(), nullable=True))
    
    # Create indexes for location fields
    op.create_index(op.f('ix_users_province'), 'users', ['province'], unique=False)
    op.create_index(op.f('ix_users_district'), 'users', ['district'], unique=False)
    op.create_index(op.f('ix_users_sector'), 'users', ['sector'], unique=False)


def downgrade():
    # Drop indexes
    op.drop_index(op.f('ix_users_sector'), table_name='users')
    op.drop_index(op.f('ix_users_district'), table_name='users')
    op.drop_index(op.f('ix_users_province'), table_name='users')
    
    # Drop columns from users
    op.drop_column('users', 'sector')
    op.drop_column('users', 'district')
    op.drop_column('users', 'province')
    
    # Drop schools table
    op.drop_index(op.f('ix_schools_sector'), table_name='schools')
    op.drop_index(op.f('ix_schools_district'), table_name='schools')
    op.drop_index(op.f('ix_schools_province'), table_name='schools')
    op.drop_index(op.f('ix_schools_name'), table_name='schools')
    op.drop_index(op.f('ix_schools_id'), table_name='schools')
    op.drop_table('schools')
