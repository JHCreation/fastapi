"""empty message

Revision ID: 91c0fb06510b
Revises: 011b1e0f1044
Create Date: 2024-10-11 19:46:34.292378

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '91c0fb06510b'
down_revision: Union[str, None] = '011b1e0f1044'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('key', table_name='works')
    op.drop_table('works')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('works',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('key', mysql.VARCHAR(length=50), nullable=False),
    sa.Column('title', mysql.VARCHAR(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('key', 'works', ['key'], unique=True)
    # ### end Alembic commands ###
