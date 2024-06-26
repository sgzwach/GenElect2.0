"""empty message

Revision ID: c3d8073a10d8
Revises: 
Create Date: 2021-06-10 19:49:58.728085

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c3d8073a10d8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('buildings',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('date_modified', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('configs',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('date_modified', sa.DateTime(), nullable=True),
    sa.Column('key', sa.Text(), nullable=True),
    sa.Column('value', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('electives',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('date_modified', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('description', sa.String(length=500), nullable=True),
    sa.Column('learning_objective', sa.String(length=500), nullable=True),
    sa.Column('can_retake', sa.Boolean(), nullable=True),
    sa.Column('elective_difficulty', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('notifications',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('date_modified', sa.DateTime(), nullable=True),
    sa.Column('title', sa.String(length=100), nullable=True),
    sa.Column('notification', sa.String(length=1000), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('date_modified', sa.DateTime(), nullable=True),
    sa.Column('username', sa.String(length=100), nullable=True),
    sa.Column('full_name', sa.String(length=100), nullable=True),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('role', sa.String(length=32), nullable=False),
    sa.Column('password', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('completions',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('date_modified', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('elective_id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['elective_id'], ['electives.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('prerequisites',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('date_modified', sa.DateTime(), nullable=True),
    sa.Column('elective_id', sa.Integer(), nullable=False),
    sa.Column('prerequisite_elective_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['elective_id'], ['electives.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('rooms',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('date_modified', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('building_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['building_id'], ['buildings.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cores',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('date_modified', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('description', sa.String(length=500), nullable=True),
    sa.Column('building', sa.String(length=100), nullable=True),
    sa.Column('room_id', sa.Integer(), nullable=False),
    sa.Column('core_period', sa.Integer(), nullable=True),
    sa.Column('core_difficulty', sa.String(length=100), nullable=True),
    sa.Column('instructor_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['instructor_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['room_id'], ['rooms.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('events',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('date_modified', sa.DateTime(), nullable=True),
    sa.Column('start_time', sa.DateTime(), nullable=False),
    sa.Column('end_time', sa.DateTime(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('room_id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=250), nullable=False),
    sa.ForeignKeyConstraint(['room_id'], ['rooms.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('offerings',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('date_modified', sa.DateTime(), nullable=True),
    sa.Column('period_start', sa.Integer(), nullable=True),
    sa.Column('period_length', sa.Integer(), nullable=True),
    sa.Column('room_id', sa.Integer(), nullable=False),
    sa.Column('instructor_id', sa.Integer(), nullable=False),
    sa.Column('current_count', sa.Integer(), nullable=True),
    sa.Column('capacity', sa.Integer(), nullable=True),
    sa.Column('elective_id', sa.Integer(), nullable=False),
    sa.Column('start_time', sa.DateTime(), nullable=False),
    sa.Column('end_time', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['elective_id'], ['electives.id'], ),
    sa.ForeignKeyConstraint(['instructor_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['room_id'], ['rooms.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('coreattends',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('date_modified', sa.DateTime(), nullable=True),
    sa.Column('student_id', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(length=25), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('core_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['core_id'], ['cores.id'], ),
    sa.ForeignKeyConstraint(['student_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('coreregistrations',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('date_modified', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('core_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['core_id'], ['cores.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('offeringattends',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('date_modified', sa.DateTime(), nullable=True),
    sa.Column('offering_id', sa.Integer(), nullable=False),
    sa.Column('student_id', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(length=25), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['offering_id'], ['offerings.id'], ),
    sa.ForeignKeyConstraint(['student_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('registrations',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('date_modified', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('offering_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['offering_id'], ['offerings.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('registrations')
    op.drop_table('offeringattends')
    op.drop_table('coreregistrations')
    op.drop_table('coreattends')
    op.drop_table('offerings')
    op.drop_table('events')
    op.drop_table('cores')
    op.drop_table('rooms')
    op.drop_table('prerequisites')
    op.drop_table('completions')
    op.drop_table('users')
    op.drop_table('notifications')
    op.drop_table('electives')
    op.drop_table('configs')
    op.drop_table('buildings')
    # ### end Alembic commands ###
