"""remove sickle cell status

Revision ID: 628f40244e30
Revises: 0c6b9de93c94
Create Date: 2023-11-22 18:33:40.256611

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '628f40244e30'
down_revision = '0c6b9de93c94'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('medical_history', schema=None) as batch_op:
        batch_op.drop_column('sickle_cell_status')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('medical_history', schema=None) as batch_op:
        batch_op.add_column(sa.Column('sickle_cell_status', sa.VARCHAR(), autoincrement=False, nullable=True))

    # ### end Alembic commands ###
