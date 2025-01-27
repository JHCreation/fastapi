"""empty message

Revision ID: 9859e1dd61f3
Revises: 2380762fb696
Create Date: 2025-01-26 13:27:28.554997

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '9859e1dd61f3'
down_revision: Union[str, None] = '2380762fb696'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_user_permission', table_name='user')
    op.drop_index('ix_user_sns_type', table_name='user')
    op.drop_index('ix_user_usertype', table_name='user')
    op.drop_index('sns_id', table_name='user')
    op.drop_index('userid', table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('userid', mysql.VARCHAR(length=100), nullable=False),
    sa.Column('password', mysql.VARCHAR(length=500), nullable=True),
    sa.Column('email', mysql.VARCHAR(length=50), nullable=False),
    sa.Column('phone', mysql.VARCHAR(length=13), nullable=False),
    sa.Column('username', mysql.VARCHAR(length=50), nullable=True),
    sa.Column('usertype', mysql.VARCHAR(length=20), nullable=False),
    sa.Column('permission', mysql.VARCHAR(length=20), nullable=False),
    sa.Column('nickname', mysql.VARCHAR(length=100), nullable=True),
    sa.Column('modify_date', mysql.DATETIME(), nullable=False),
    sa.Column('create_date', mysql.DATETIME(), nullable=False),
    sa.Column('sns_type', mysql.VARCHAR(length=50), nullable=False),
    sa.Column('sns_id', mysql.VARCHAR(length=50), nullable=False),
    sa.Column('sns_name', mysql.VARCHAR(length=50), nullable=True),
    sa.Column('sns_gender', mysql.VARCHAR(length=10), nullable=True),
    sa.Column('sns_age', mysql.VARCHAR(length=10), nullable=True),
    sa.Column('sns_birthyear', mysql.VARCHAR(length=10), nullable=True),
    sa.Column('sns_birthday', mysql.VARCHAR(length=10), nullable=True),
    sa.Column('sns_connect_date', mysql.VARCHAR(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('userid', 'user', ['userid'], unique=True)
    op.create_index('sns_id', 'user', ['sns_id'], unique=True)
    op.create_index('ix_user_usertype', 'user', ['usertype'], unique=False)
    op.create_index('ix_user_sns_type', 'user', ['sns_type'], unique=False)
    op.create_index('ix_user_permission', 'user', ['permission'], unique=False)
    # ### end Alembic commands ###
