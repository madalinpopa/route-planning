"""empty message

Revision ID: ffa476fa4b1d
Revises: 1c8b4d9ec675
Create Date: 2024-06-23 14:28:30.128417

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ffa476fa4b1d'
down_revision = '1c8b4d9ec675'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password', sa.String(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('password')

    # ### end Alembic commands ###
