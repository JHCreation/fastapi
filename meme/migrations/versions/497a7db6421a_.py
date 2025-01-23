"""empty message

Revision ID: 497a7db6421a
Revises: 3667f5bdf3b3
Create Date: 2024-04-07 12:57:21.481659

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '497a7db6421a'
down_revision: Union[str, None] = '3667f5bdf3b3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'sns_connect_date',
               existing_type=mysql.VARCHAR(length=50),
               nullable=True)
    op.drop_index('sns_connect_date', table_name='user')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('sns_connect_date', 'user', ['sns_connect_date'], unique=True)
    op.alter_column('user', 'sns_connect_date',
               existing_type=mysql.VARCHAR(length=50),
               nullable=False)
    # ### end Alembic commands ###
