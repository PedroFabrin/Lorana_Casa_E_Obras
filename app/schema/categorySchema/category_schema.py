from pydantic import BaseModel
from typing import Optional
from app.schema.pagination import PaginationParams
from app.model.categoryModel.category_model import CategoryStatus


class CategoryCreate(BaseModel):
    section_id: int
    nome: str
    descricao: Optional[str] = None
    status: CategoryStatus = CategoryStatus.ativo


class CategoryFilter(PaginationParams):
    section_id: Optional[int] = None
    nome: Optional[str] = None
    status: Optional[CategoryStatus] = None


class CategoryUpdate(BaseModel):
    category_id: int
    section_id: Optional[int] = None
    nome: Optional[str] = None
    descricao: Optional[str] = None
    status: Optional[CategoryStatus] = None


class CategoryResponse(BaseModel):
    id: int
    section_id: int
    nome: str
    descricao: Optional[str] = None
    status: CategoryStatus

    model_config = {"from_attributes": True}


class CategoryListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    data: list[CategoryResponse]
