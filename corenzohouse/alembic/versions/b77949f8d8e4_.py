"""empty message

Revision ID: b77949f8d8e4
Revises: 05b125b468ab
Create Date: 2025-02-01 14:28:45.078852

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b77949f8d8e4'
down_revision: Union[str, None] = '05b125b468ab'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_webpush_endpoint'), 'webpush', ['endpoint'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_webpush_endpoint'), table_name='webpush')
    # ### end Alembic commands ###
