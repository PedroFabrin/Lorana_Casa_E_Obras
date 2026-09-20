from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.model.userModel.user_model import UserModel, UserRole
from app.model.revokedTokenModel.revoked_token_model import RevokedTokenModel
from app.utils.jwt import decode_token_payload

bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> UserModel:
    token = credentials.credentials
    payload = decode_token_payload(token)

    if payload is None or payload.get("sub") is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido ou expirado")

    jti = payload.get("jti")
    if jti:
        revoked = db.query(RevokedTokenModel).filter(
            RevokedTokenModel.jti == jti, RevokedTokenModel.deleted_at == None,
        ).first()
        if revoked:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Sessão encerrada, faça login novamente")

    user = db.query(UserModel).filter(UserModel.id == int(payload["sub"]), UserModel.deleted_at == None).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não encontrado")

    return user


def get_current_admin(current_user: UserModel = Depends(get_current_user)) -> UserModel:
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso restrito a administradores")
    return current_user
