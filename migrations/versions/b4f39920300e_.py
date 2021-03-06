"""empty message

Revision ID: b4f39920300e
Revises: 37d5cec33210
Create Date: 2018-06-09 15:00:34.698914

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b4f39920300e'
down_revision = '37d5cec33210'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('desc', sa.Text(), nullable=True))
    op.add_column('users', sa.Column('fullname', sa.String(length=64), nullable=True))
    op.add_column('users', sa.Column('last_visit', sa.DateTime(), nullable=True))
    op.add_column('users', sa.Column('location', sa.String(length=64), nullable=True))
    op.add_column('users', sa.Column('member_since', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'member_since')
    op.drop_column('users', 'location')
    op.drop_column('users', 'last_visit')
    op.drop_column('users', 'fullname')
    op.drop_column('users', 'desc')
    # ### end Alembic commands ###
