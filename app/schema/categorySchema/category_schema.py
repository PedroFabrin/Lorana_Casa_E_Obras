from pydantic import BaseModel
from typing import Optional
from app.schema.pagination import PaginationParams


class CategoryCreate(BaseModel):
    nome: str
    descricao: Optional[str] = None


class CategoryFilter(PaginationParams):
    nome: Optional[str] = None


class CategoryUpdate(BaseModel):
    category_id: int
    nome: Optional[str] = None
    descricao: Optional[str] = None


class CategoryResponse(BaseModel):
    id: int
    nome: str
    descricao: Optional[str] = None

    model_config = {"from_attributes": True}


class CategoryListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    data: list[CategoryResponse]
