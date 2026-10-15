"""Cria ou atualiza o usuário admin a partir de ADMIN_EMAIL/ADMIN_PASSWORD.

Diferente da migration de seed (que só insere o admin uma vez), este script
sincroniza o banco com os valores atuais das variáveis de ambiente:
- se já existe um usuário ativo com ADMIN_EMAIL, atualiza a senha e garante role admin;
- se não existe, cria o admin.

Uso:
    docker exec lorana_api python scripts/create_admin.py
    fly ssh console -a lorana-api -C "python /app/scripts/create_admin.py"
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app.model  # noqa: F401 — registra todos os models (relationships)
from app.database import SessionLocal
from app.model.userModel.user_model import UserModel, UserRole
from app.utils.security import hash_password


def main():
    admin_email = os.environ.get("ADMIN_EMAIL")
    admin_password = os.environ.get("ADMIN_PASSWORD")
    if not admin_email or not admin_password:
        sys.exit("ADMIN_EMAIL e ADMIN_PASSWORD precisam estar definidos.")

    db = SessionLocal()
    try:
        user = db.query(UserModel).filter(
            UserModel.email == admin_email,
            UserModel.deleted_at == None,
        ).first()

        if user:
            user.password = hash_password(admin_password)
            user.role = UserRole.admin
            action = "atualizado"
        else:
            user = UserModel(
                name="Administrador",
                email=admin_email,
                cpf="00000000000",
                password=hash_password(admin_password),
                role=UserRole.admin,
            )
            db.add(user)
            action = "criado"

        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

    print(f"Admin {admin_email} {action}.")


if __name__ == "__main__":
    main()
