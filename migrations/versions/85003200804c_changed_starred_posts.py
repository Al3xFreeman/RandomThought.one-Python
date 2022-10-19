"""Changed starred posts

Revision ID: 85003200804c
Revises: 4522b9b22bb8
Create Date: 2022-10-19 14:06:53.441853

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '85003200804c'
down_revision = '4522b9b22bb8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'stars')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('stars', sa.INTEGER(), nullable=True))
    # ### end Alembic commands ###