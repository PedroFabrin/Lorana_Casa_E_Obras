from datetime import datetime
from sqlalchemy.orm import Session
from app.model.userModel.user_model import UserModel
from app.model.revokedTokenModel.revoked_token_model import RevokedTokenModel
from app.schema.authSchema.auth_schema import LoginRequest, LoginResponse
from app.utils.security import verify_password
from app.utils.jwt import create_access_token, decode_token_payload


def login(db: Session, data: LoginRequest):
    try:
        user = db.query(UserModel).filter(UserModel.email == data.email, UserModel.deleted_at == None).first()
        if not user:
            return None, "E-mail ou senha inválidos"

        if not verify_password(data.password, user.password):
            return None, "E-mail ou senha inválidos"

        token = create_access_token(user.id)
        result = LoginResponse(access_token=token)
        return {"status": "success", "data": result.model_dump()}, None
    except Exception as e:
        return None, str(e)


def logout(db: Session, token: str):
    try:
        payload = decode_token_payload(token)
        if not payload or not payload.get("jti"):
            return None, "Token inválido"

        jti = payload["jti"]
        already_revoked = db.query(RevokedTokenModel).filter(
            RevokedTokenModel.jti == jti, RevokedTokenModel.deleted_at == None,
        ).first()
        if not already_revoked:
            expires_at = datetime.utcfromtimestamp(payload["exp"]) if payload.get("exp") else datetime.utcnow()
            db.add(RevokedTokenModel(jti=jti, user_id=int(payload["sub"]), expires_at=expires_at))
            db.commit()

        return {"status": "success", "data": {"message": "Logout realizado com sucesso"}}, None
    except Exception as e:
        return None, str(e)
