"""create address table

Revision ID: 8118f1fad900
Revises: 239fb324bc8a
Create Date: 2026-04-21 19:00:55.401689

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

revision: str = '8118f1fad900'
down_revision: Union[str, None] = '239fb324bc8a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('adress',
    sa.Column('id', mysql.BIGINT(unsigned=True), autoincrement=True, nullable=False),
    sa.Column('user_id', mysql.BIGINT(unsigned=True), nullable=False),
    sa.Column('rua', sa.VARCHAR(length=255), nullable=False),
    sa.Column('numero', sa.VARCHAR(length=10), nullable=False),
    sa.Column('cep', sa.VARCHAR(length=8), nullable=False),
    sa.Column('cidade', sa.VARCHAR(length=255), nullable=False),
    sa.Column('uf', sa.VARCHAR(length=2), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_adress_id'), 'adress', ['id'], unique=False)
    op.create_index(op.f('ix_adress_user_id'), 'adress', ['user_id'], unique=False)



def downgrade() -> None:
    op.drop_index(op.f('ix_adress_user_id'), table_name='adress')
    op.drop_index(op.f('ix_adress_id'), table_name='adress')
    op.drop_table('adress')
