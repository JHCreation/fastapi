"""empty message

Revision ID: 000738d1ae92
Revises: f5adbedc3e67
Create Date: 2025-06-14 15:06:17.535385

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '000738d1ae92'
down_revision: Union[str, None] = 'f5adbedc3e67'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('_users', 'modify_date',
               existing_type=mysql.DATETIME(),
               nullable=True)
    op.alter_column('mapoclean_works', 'modify_date',
               existing_type=mysql.DATETIME(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('mapoclean_works', 'modify_date',
               existing_type=mysql.DATETIME(),
               nullable=False)
    op.alter_column('_users', 'modify_date',
               existing_type=mysql.DATETIME(),
               nullable=False)
    # ### end Alembic commands ###
