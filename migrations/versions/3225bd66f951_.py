"""empty message

Revision ID: 3225bd66f951
Revises: 88f141fcec83
Create Date: 2024-06-24 19:44:15.170518

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3225bd66f951'
down_revision = '88f141fcec83'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('drivers', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('phone', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('drivers', schema=None) as batch_op:
        batch_op.drop_column('phone')
        batch_op.drop_column('email')

    # ### end Alembic commands ###
