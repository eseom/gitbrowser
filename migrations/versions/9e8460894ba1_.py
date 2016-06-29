"""empty message

Revision ID: 9e8460894ba1
Revises: 09dbb4e92fab
Create Date: 2016-06-23 22:14:19.291160

"""

# revision identifiers, used by Alembic.
revision = '9e8460894ba1'
down_revision = '09dbb4e92fab'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('repos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('group', sa.Unicode(length=256), nullable=False),
    sa.Column('name', sa.Unicode(length=256), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('type', sa.Integer(), nullable=False),
    sa.Column('description', sa.UnicodeText(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('reporoles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('repo_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('credential', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['repo_id'], ['repos.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('reporoles')
    op.drop_table('repos')
    ### end Alembic commands ###