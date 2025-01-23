"""empty message

Revision ID: 4b93166c2db5
Revises: b654382dfe5b
Create Date: 2024-03-18 15:25:38.338935

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '4b93166c2db5'
down_revision: Union[str, None] = 'b654382dfe5b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'userid',
               existing_type=mysql.VARCHAR(length=170),
               type_=sa.String(length=100),
               existing_nullable=False)
    op.drop_column('user', 'user_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('user_id', mysql.VARCHAR(length=170), nullable=False))
    op.alter_column('user', 'userid',
               existing_type=sa.String(length=100),
               type_=mysql.VARCHAR(length=170),
               existing_nullable=False)
    # ### end Alembic commands ###
