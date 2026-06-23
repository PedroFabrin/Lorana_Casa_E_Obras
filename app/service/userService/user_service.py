from datetime import datetime
from sqlalchemy.orm import Session
from app.model.userModel.user_model import UserModel, UserRole
from app.schema.userSchema.user_schema import UserCreate, UserUpdate, UserFilter, UserResponse, UserListResponse
from app.utils.security import hash_password


def create_user(db: Session, data: UserCreate):
    try:
        if db.query(UserModel).filter(UserModel.email == data.email, UserModel.deleted_at == None).first():
            return None, "E-mail já cadastrado"
        if db.query(UserModel).filter(UserModel.cpf == data.cpf, UserModel.deleted_at == None).first():
            return None, "CPF já cadastrado"

        user = UserModel(
            name=data.name,
            email=data.email,
            cpf=data.cpf,
            password=hash_password(data.password),
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        result = UserResponse.model_validate(user)
        return {"status": "success", "data": result.model_dump(mode='json')}, None
    except Exception as e:
        return None, str(e)


def get_user(db: Session, user_id: int):
    try:
        user = db.query(UserModel).filter(UserModel.id == user_id, UserModel.deleted_at == None).first()
        if not user:
            return None, "Usuário não encontrado"

        result = UserResponse.model_validate(user)
        return {"status": "success", "data": result.model_dump(mode='json')}, None
    except Exception as e:
        return None, str(e)


def get_users(db: Session, filters: UserFilter):
    try:
        query = db.query(UserModel).filter(UserModel.deleted_at == None)

        if filters.name:
            query = query.filter(UserModel.name.ilike(f"%{filters.name}%"))
        if filters.email:
            query = query.filter(UserModel.email.ilike(f"%{filters.email}%"))
        if filters.cpf:
            query = query.filter(UserModel.cpf == filters.cpf)
        if filters.role:
            query = query.filter(UserModel.role == filters.role)

        total = query.count()
        offset = (filters.page - 1) * filters.page_size
        users = query.offset(offset).limit(filters.page_size).all()

        result = UserListResponse(
            total=total,
            page=filters.page,
            page_size=filters.page_size,
            data=[UserResponse.model_validate(u) for u in users],
        )
        return {"status": "success", "data": result.model_dump(mode='json')}, None
    except Exception as e:
        return None, str(e)


def update_user(db: Session, data: UserUpdate, current_user: UserModel):
    try:
        is_admin = current_user.role == UserRole.admin

        if not is_admin and current_user.id != data.user_id:
            return None, "Você só pode alterar a própria conta"
        if not is_admin and data.role is not None:
            return None, "Você não pode alterar seu próprio papel de acesso"

        user = db.query(UserModel).filter(UserModel.id == data.user_id, UserModel.deleted_at == None).first()
        if not user:
            return None, "Usuário não encontrado"

        fields = data.model_dump(exclude_none=True, exclude={"user_id"})
        if "password" in fields:
            fields["password"] = hash_password(fields["password"])

        for field, value in fields.items():
            setattr(user, field, value)

        db.commit()
        db.refresh(user)

        result = UserResponse.model_validate(user)
        return {"status": "success", "data": result.model_dump(mode='json')}, None
    except Exception as e:
        return None, str(e)


def delete_user(db: Session, user_id: int, current_user: UserModel):
    try:
        if current_user.role != UserRole.admin and current_user.id != user_id:
            return None, "Você só pode excluir a própria conta"

        user = db.query(UserModel).filter(UserModel.id == user_id, UserModel.deleted_at == None).first()
        if not user:
            return None, "Usuário não encontrado"

        user.deleted_at = datetime.now()
        db.commit()
        return {"status": "success", "message": "Usuário deletado com sucesso"}, None
    except Exception as e:
        return None, str(e)
