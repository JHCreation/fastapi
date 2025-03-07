"""empty message

Revision ID: 48bf73a20821
Revises: e24d41dae8c0
Create Date: 2025-02-20 15:08:42.343362

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '48bf73a20821'
down_revision: Union[str, None] = 'e24d41dae8c0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('name', table_name='reviewers')
    op.create_index(op.f('ix_reviewers_name'), 'reviewers', ['name'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_reviewers_name'), table_name='reviewers')
    op.create_index('name', 'reviewers', ['name'], unique=True)
    # ### end Alembic commands ###
