"""initial migration

Revision ID: 29b556e2db06
Revises: 
Create Date: 2024-05-22 21:54:21.562372

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '29b556e2db06'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('countries',
    sa.Column('id', sa.String(length=3), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('password_hash', sa.String(length=256), nullable=False),
    sa.Column('profile_image', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_users_username'), ['username'], unique=True)

    op.create_table('videos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tmdb_id', sa.Integer(), nullable=False),
    sa.Column('media_type', sa.String(length=10), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('videos', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_videos_media_type'), ['media_type'], unique=False)
        batch_op.create_index(batch_op.f('ix_videos_tmdb_id'), ['tmdb_id'], unique=False)

    op.create_table('video_lists',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('video_lists', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_video_lists_name'), ['name'], unique=False)
        batch_op.create_index(batch_op.f('ix_video_lists_user_id'), ['user_id'], unique=False)

    op.create_table('video_list_videos',
    sa.Column('video_id', sa.Integer(), nullable=False),
    sa.Column('video_list_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['video_id'], ['videos.id'], ),
    sa.ForeignKeyConstraint(['video_list_id'], ['video_lists.id'], ),
    sa.PrimaryKeyConstraint('video_id', 'video_list_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('video_list_videos')
    with op.batch_alter_table('video_lists', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_video_lists_user_id'))
        batch_op.drop_index(batch_op.f('ix_video_lists_name'))

    op.drop_table('video_lists')
    with op.batch_alter_table('videos', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_videos_tmdb_id'))
        batch_op.drop_index(batch_op.f('ix_videos_media_type'))

    op.drop_table('videos')
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_users_username'))

    op.drop_table('users')
    op.drop_table('countries')
    # ### end Alembic commands ###
