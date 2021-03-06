"""auto generate the likes and comments tables

Revision ID: 6dacd6729e89
Revises: d1d70d5a438a
Create Date: 2022-02-14 23:09:21.556542

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6dacd6729e89'
down_revision = 'd1d70d5a438a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comments',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('content', sa.String(), nullable=True),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.Column('com_owner_id', sa.Integer(), nullable=True),
                    sa.Column('com_post_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(
                        ['com_owner_id'], ['users.id'], ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(
                        ['com_post_id'], ['posts.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('likes',
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('post_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(
                        ['post_id'], ['posts.id'], ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(
                        ['user_id'], ['users.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('user_id', 'post_id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('likes')
    op.drop_table('comments')
    # ### end Alembic commands ###
