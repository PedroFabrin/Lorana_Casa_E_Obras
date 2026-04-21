"""create product and category  table

Revision ID: a240d7b87994
Revises: 8118f1fad900
Create Date: 2026-04-21 19:17:18.737180

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

revision: str = 'a240d7b87994'
down_revision: Union[str, None] = '8118f1fad900'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('category',
    sa.Column('id', mysql.BIGINT(unsigned=True), autoincrement=True, nullable=False),
    sa.Column('nome', sa.VARCHAR(length=255), nullable=False),
    sa.Column('descricao', sa.TEXT(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_category_id'), 'category', ['id'], unique=False)
    op.create_index(op.f('ix_category_nome'), 'category', ['nome'], unique=False)
    op.create_table('product',
    sa.Column('id', mysql.BIGINT(unsigned=True), autoincrement=True, nullable=False),
    sa.Column('category_id', mysql.BIGINT(unsigned=True), nullable=False),
    sa.Column('nome', sa.VARCHAR(length=255), nullable=False),
    sa.Column('descricao', sa.TEXT(), nullable=True),
    sa.Column('preco', sa.DECIMAL(precision=10, scale=2), nullable=False),
    sa.Column('sku', sa.VARCHAR(length=100), nullable=False),
    sa.Column('quantidade_estoque', mysql.BIGINT(unsigned=True), nullable=False),
    sa.Column('status', sa.Enum('ativo', 'inativo', name='productstatus'), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_product_category_id'), 'product', ['category_id'], unique=False)
    op.create_index(op.f('ix_product_id'), 'product', ['id'], unique=False)
    op.create_index(op.f('ix_product_nome'), 'product', ['nome'], unique=False)
    op.create_index(op.f('ix_product_sku'), 'product', ['sku'], unique=True)



def downgrade() -> None:
    op.drop_index(op.f('ix_product_sku'), table_name='product')
    op.drop_index(op.f('ix_product_nome'), table_name='product')
    op.drop_index(op.f('ix_product_id'), table_name='product')
    op.drop_index(op.f('ix_product_category_id'), table_name='product')
    op.drop_table('product')
    op.drop_index(op.f('ix_category_nome'), table_name='category')
    op.drop_index(op.f('ix_category_id'), table_name='category')
    op.drop_table('category')

