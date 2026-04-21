"""add created_at updated_at deleted_at to all tables

Revision ID: a8653b2e8397
Revises: a240d7b87994
Create Date: 2026-04-21 19:47:15.342947

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'a8653b2e8397'
down_revision: Union[str, None] = 'a240d7b87994'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('adress', sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.add_column('adress', sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.add_column('adress', sa.Column('deleted_at', sa.DateTime(), nullable=True))
    op.add_column('category', sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.add_column('category', sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.add_column('category', sa.Column('deleted_at', sa.DateTime(), nullable=True))
    op.add_column('product', sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.add_column('product', sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.add_column('product', sa.Column('deleted_at', sa.DateTime(), nullable=True))
    op.add_column('user', sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.add_column('user', sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.add_column('user', sa.Column('deleted_at', sa.DateTime(), nullable=True))



def downgrade() -> None:
    op.drop_column('user', 'deleted_at')
    op.drop_column('user', 'updated_at')
    op.drop_column('user', 'created_at')
    op.drop_column('product', 'deleted_at')
    op.drop_column('product', 'updated_at')
    op.drop_column('product', 'created_at')
    op.drop_column('category', 'deleted_at')
    op.drop_column('category', 'updated_at')
    op.drop_column('category', 'created_at')
    op.drop_column('adress', 'deleted_at')
    op.drop_column('adress', 'updated_at')
    op.drop_column('adress', 'created_at')

