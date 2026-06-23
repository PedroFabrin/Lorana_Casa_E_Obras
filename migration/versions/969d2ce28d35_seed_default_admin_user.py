"""seed default admin user

Revision ID: 969d2ce28d35
Revises: dbe179e98607
Create Date: 2026-06-22 21:49:42.262800

"""
import os
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from app.utils.security import hash_password

revision: str = '969d2ce28d35'
down_revision: Union[str, None] = 'dbe179e98607'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()

    admin_email = os.environ.get("ADMIN_EMAIL")
    admin_password = os.environ.get("ADMIN_PASSWORD")
    if not admin_email or not admin_password:
        return

    exists = bind.execute(
        sa.text("SELECT id FROM user WHERE email = :email"), {"email": admin_email}
    ).first()
    if exists:
        return

    bind.execute(
        sa.text(
            "INSERT INTO user (name, email, cpf, password, role, created_at, updated_at) "
            "VALUES ('Administrador', :email, '00000000000', :password, 'admin', NOW(), NOW())"
        ),
        {"email": admin_email, "password": hash_password(admin_password)},
    )


def downgrade() -> None:
    bind = op.get_bind()
    admin_email = os.environ.get("ADMIN_EMAIL")
    if admin_email:
        bind.execute(sa.text("DELETE FROM user WHERE email = :email AND role = 'admin'"), {"email": admin_email})
