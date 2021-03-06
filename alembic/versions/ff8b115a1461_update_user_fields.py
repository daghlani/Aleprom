"""update_user_fields

Revision ID: ff8b115a1461
Revises: e99001c60151
Create Date: 2022-06-05 19:00:09.796317

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ff8b115a1461'
down_revision = 'e99001c60151'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('info', sa.Boolean(), nullable=True))
    op.add_column('users', sa.Column('warning', sa.Boolean(), nullable=True))
    op.add_column('users', sa.Column('error', sa.Boolean(), nullable=True))
    op.add_column('users', sa.Column('critical', sa.Boolean(), nullable=True))
    op.drop_column('users', 'critical_st')
    op.drop_column('users', 'error_st')
    op.drop_column('users', 'info_st')
    op.drop_column('users', 'warning_st')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('warning_st', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('users', sa.Column('info_st', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('users', sa.Column('error_st', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('users', sa.Column('critical_st', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_column('users', 'critical')
    op.drop_column('users', 'error')
    op.drop_column('users', 'warning')
    op.drop_column('users', 'info')
    # ### end Alembic commands ###
