"""Updated Users and Posts"

Revision ID: 63d5226e937a
Revises: fbcda50ea154
Create Date: 2022-10-19 02:13:16.514081

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '63d5226e937a'
down_revision = 'fbcda50ea154'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('stars', sa.Integer(), nullable=True))
    op.add_column('user', sa.Column('stars', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'stars')
    op.drop_column('post', 'stars')
    # ### end Alembic commands ###
