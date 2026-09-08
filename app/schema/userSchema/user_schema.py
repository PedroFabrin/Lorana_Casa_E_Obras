from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from app.schema.pagination import PaginationParams
from app.model.userModel.user_model import UserRole


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    cpf: str
    password: str = Field(min_length=8)


class UserFilter(PaginationParams):
    name: Optional[str] = None
    email: Optional[str] = None
    cpf: Optional[str] = None
    role: Optional[UserRole] = None


class UserUpdate(BaseModel):
    user_id: int
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    cpf: Optional[str] = None
    password: Optional[str] = Field(default=None, min_length=8)
    role: Optional[UserRole] = None


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    cpf: str
    role: UserRole

    model_config = {"from_attributes": True}


class UserListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    data: list[UserResponse]
