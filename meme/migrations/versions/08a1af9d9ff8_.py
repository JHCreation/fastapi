"""empty message

Revision ID: 08a1af9d9ff8
Revises: d948994b35cd
Create Date: 2024-04-05 12:41:48.871674

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '08a1af9d9ff8'
down_revision: Union[str, None] = 'd948994b35cd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'nickname',
               existing_type=mysql.VARCHAR(length=50),
               type_=sa.String(length=100),
               nullable=True)
    op.drop_index('nickname', table_name='user')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('nickname', 'user', ['nickname'], unique=True)
    op.alter_column('user', 'nickname',
               existing_type=sa.String(length=100),
               type_=mysql.VARCHAR(length=50),
               nullable=False)
    # ### end Alembic commands ###
