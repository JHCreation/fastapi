"""empty message

Revision ID: 1c7c13d28df2
Revises: d26c3895ceda
Create Date: 2024-11-25 14:05:00.097272

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '1c7c13d28df2'
down_revision: Union[str, None] = 'd26c3895ceda'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('wine',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('key', mysql.VARCHAR(length=50), nullable=False),
    sa.Column('name', mysql.VARCHAR(length=50), nullable=True),
    sa.Column('content', mysql.LONGTEXT(), nullable=True),
    sa.Column('create_date', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('key')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('wine')
    # ### end Alembic commands ###
