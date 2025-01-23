"""empty message

Revision ID: bab5fc3fbed6
Revises: b1c87ef596c7
Create Date: 2024-10-01 16:37:21.499849

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'bab5fc3fbed6'
down_revision: Union[str, None] = 'b1c87ef596c7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('key', table_name='portfolio')
    op.drop_table('portfolio')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('portfolio',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('key', mysql.VARCHAR(length=50), nullable=False),
    sa.Column('name', mysql.VARCHAR(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('key', 'portfolio', ['key'], unique=True)
    # ### end Alembic commands ###
