"""empty message

Revision ID: 10d75f0eebe1
Revises: 932e0796089c
Create Date: 2024-03-08 13:48:06.563087

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '10d75f0eebe1'
down_revision: Union[str, None] = '932e0796089c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('answer', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'answer', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'answer', type_='foreignkey')
    op.drop_column('answer', 'user_id')
    # ### end Alembic commands ###
