"""add school_code and gender to schools

Revision ID: add_school_code_gender
Revises: add_trades_fields
Create Date: 2025-01-04 20:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_school_code_gender'
down_revision = 'add_trades_fields'
branch_labels = None
depends_on = None


def upgrade():
    # Add school_code and gender columns to schools table
    with op.batch_alter_table('schools', schema=None) as batch_op:
        batch_op.add_column(sa.Column('school_code', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('gender', sa.String(), nullable=True))


def downgrade():
    # Remove columns
    with op.batch_alter_table('schools', schema=None) as batch_op:
        batch_op.drop_column('gender')
        batch_op.drop_column('school_code')
