"""empty message

Revision ID: 329e750a4694
Revises: fc9327f0b158
Create Date: 2021-06-12 12:33:20.623732

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '329e750a4694'
down_revision = 'fc9327f0b158'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('loginattempts',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('date_modified', sa.DateTime(), nullable=True),
    sa.Column('ip', sa.String(), nullable=True),
    sa.Column('attempts', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('loginattempts')
    # ### end Alembic commands ###
