"""empty message

Revision ID: 9e9a975ffe87
Revises: 2a9bf32a8c0e
Create Date: 2024-06-27 06:21:32.102478

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9e9a975ffe87'
down_revision = '2a9bf32a8c0e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('routes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('initial_km', sa.Float(), nullable=False))
        batch_op.add_column(sa.Column('start_address', sa.String(), nullable=False))
        batch_op.add_column(sa.Column('end_address', sa.String(), nullable=False))
        batch_op.drop_column('start_from')
        batch_op.drop_column('end_to')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('routes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('end_to', sa.VARCHAR(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('start_from', sa.VARCHAR(), autoincrement=False, nullable=False))
        batch_op.drop_column('end_address')
        batch_op.drop_column('start_address')
        batch_op.drop_column('initial_km')

    # ### end Alembic commands ###