from sqlalchemy.orm import Session
from app.model.userModel.user_model import UserModel
from app.schema.authSchema.auth_schema import LoginRequest, LoginResponse
from app.utils.security import verify_password
from app.utils.jwt import create_access_token


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
