from sqlalchemy.orm import Session
from app.model.userModel.user_model import UserModel
from app.schema.userSchema.user_schema import UserCreate, UserUpdate, UserFilter, UserResponse, UserListResponse


def create_user(db: Session, data: UserCreate):
    try:
        if db.query(UserModel).filter(UserModel.email == data.email).first():
            return None, "E-mail já cadastrado"
        if db.query(UserModel).filter(UserModel.cpf == data.cpf).first():
            return None, "CPF já cadastrado"

        user = UserModel(
            name=data.name,
            email=data.email,
            cpf=data.cpf,
            password=data.password,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        result = UserResponse.model_validate(user)
        return {"status": "success", "data": result.model_dump()}, None
    except Exception as e:
        return None, str(e)


def get_user(db: Session, user_id: int):
    try:
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            return None, "Usuário não encontrado"

        result = UserResponse.model_validate(user)
        return {"status": "success", "data": result.model_dump()}, None
    except Exception as e:
        return None, str(e)


def get_users(db: Session, filters: UserFilter):
    try:
        query = db.query(UserModel)

        if filters.name:
            query = query.filter(UserModel.name.ilike(f"%{filters.name}%"))
        if filters.email:
            query = query.filter(UserModel.email.ilike(f"%{filters.email}%"))
        if filters.cpf:
            query = query.filter(UserModel.cpf == filters.cpf)

        total = query.count()
        offset = (filters.page - 1) * filters.page_size
        users = query.offset(offset).limit(filters.page_size).all()

        result = UserListResponse(
            total=total,
            page=filters.page,
            page_size=filters.page_size,
            data=[UserResponse.model_validate(u) for u in users],
        )
        return {"status": "success", "data": result.model_dump()}, None
    except Exception as e:
        return None, str(e)


def update_user(db: Session, data: UserUpdate):
    try:
        user = db.query(UserModel).filter(UserModel.id == data.user_id).first()
        if not user:
            return None, "Usuário não encontrado"

        for field, value in data.model_dump(exclude_none=True, exclude={"user_id"}).items():
            setattr(user, field, value)

        db.commit()
        db.refresh(user)

        result = UserResponse.model_validate(user)
        return {"status": "success", "data": result.model_dump()}, None
    except Exception as e:
        return None, str(e)


def delete_user(db: Session, user_id: int):
    try:
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            return None, "Usuário não encontrado"

        db.delete(user)
        db.commit()
        return {"status": "success", "message": "Usuário deletado com sucesso"}, None
    except Exception as e:
        return None, str(e)
