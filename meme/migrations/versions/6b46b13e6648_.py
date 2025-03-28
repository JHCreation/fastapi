"""empty message

Revision ID: 6b46b13e6648
Revises: 4452de7d81a2
Create Date: 2025-03-21 14:30:15.254765

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '6b46b13e6648'
down_revision: Union[str, None] = '4452de7d81a2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('works', sa.Column('thumb', mysql.MEDIUMTEXT(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('works', 'thumb')
    # ### end Alembic commands ###
