"""empty message

Revision ID: 65325782fc9f
Revises: 9aa5322fc389
Create Date: 2024-04-13 13:56:10.969201

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '65325782fc9f'
down_revision: Union[str, None] = '9aa5322fc389'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('campaign',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('biz_title', mysql.VARCHAR(length=300), nullable=False),
    sa.Column('channel', sa.String(length=50), nullable=False),
    sa.Column('type', sa.String(length=50), nullable=False),
    sa.Column('category', sa.String(length=50), nullable=False),
    sa.Column('content', mysql.MEDIUMTEXT(), nullable=False),
    sa.Column('address', mysql.VARCHAR(length=300), nullable=False),
    sa.Column('phone', sa.String(length=13), nullable=False),
    sa.Column('msg', mysql.MEDIUMTEXT(), nullable=False),
    sa.Column('keyword', sa.Text(), nullable=False),
    sa.Column('personnel', mysql.INTEGER(display_width=5), nullable=False),
    sa.Column('available_dayname', sa.String(length=100), nullable=False),
    sa.Column('unvailable_dayname', sa.String(length=100), nullable=False),
    sa.Column('available_time', sa.Text(), nullable=False),
    sa.Column('run_start_date', sa.DateTime(), nullable=False),
    sa.Column('run_end_date', sa.DateTime(), nullable=False),
    sa.Column('apply_start_date', sa.DateTime(), nullable=False),
    sa.Column('apply_end_date', sa.DateTime(), nullable=False),
    sa.Column('create_date', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_campaign_category'), 'campaign', ['category'], unique=False)
    op.create_index(op.f('ix_campaign_channel'), 'campaign', ['channel'], unique=False)
    op.create_index(op.f('ix_campaign_type'), 'campaign', ['type'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_campaign_type'), table_name='campaign')
    op.drop_index(op.f('ix_campaign_channel'), table_name='campaign')
    op.drop_index(op.f('ix_campaign_category'), table_name='campaign')
    op.drop_table('campaign')
    # ### end Alembic commands ###
