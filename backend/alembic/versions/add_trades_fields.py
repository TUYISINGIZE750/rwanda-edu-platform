"""add trades fields

Revision ID: add_trades_fields
Revises: update_to_district_only
Create Date: 2024-01-10 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision = 'add_trades_fields'
down_revision = 'add_school_fields'
branch_labels = None
depends_on = None


def upgrade():
    # Add trades column to schools table
    with op.batch_alter_table('schools', schema=None) as batch_op:
        batch_op.add_column(sa.Column('trades', sa.JSON(), nullable=True))
    
    # Add selected_trade and selected_level columns to users table
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('selected_trade', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('selected_level', sa.String(), nullable=True))


def downgrade():
    # Remove columns
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('selected_level')
        batch_op.drop_column('selected_trade')
    
    with op.batch_alter_table('schools', schema=None) as batch_op:
        batch_op.drop_column('trades')
