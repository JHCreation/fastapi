"""empty message

Revision ID: c7094f37d2c5
Revises: 0869af565c77
Create Date: 2024-04-15 14:18:07.606874

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c7094f37d2c5'
down_revision: Union[str, None] = '0869af565c77'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('permission', sa.String(length=20), nullable=False))
    op.create_index(op.f('ix_user_permission'), 'user', ['permission'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_permission'), table_name='user')
    op.drop_column('user', 'permission')
    # ### end Alembic commands ###