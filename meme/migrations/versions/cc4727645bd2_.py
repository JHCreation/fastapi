"""empty message

Revision ID: cc4727645bd2
Revises: cd574f92dbf8
Create Date: 2024-04-07 13:06:34.733480

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'cc4727645bd2'
down_revision: Union[str, None] = 'cd574f92dbf8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'phone',
               existing_type=mysql.VARCHAR(length=12),
               type_=sa.String(length=13),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'phone',
               existing_type=sa.String(length=13),
               type_=mysql.VARCHAR(length=12),
               existing_nullable=False)
    # ### end Alembic commands ###
