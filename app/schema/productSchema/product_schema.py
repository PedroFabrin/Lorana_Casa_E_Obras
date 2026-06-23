from pydantic import BaseModel
from typing import Optional
from app.schema.pagination import PaginationParams
from app.model.productModel.product_model import ProductStatus


class ProductCreate(BaseModel):
    category_id: int
    nome: str
    descricao: Optional[str] = None
    preco: float
    preco_promocional: Optional[float] = None
    sku: str
    quantidade_estoque: int = 0
    estoque_minimo: int = 5
    peso: Optional[float] = None
    dimensoes: Optional[str] = None
    status: ProductStatus = ProductStatus.ativo


class ProductFilter(PaginationParams):
    category_id: Optional[int] = None
    nome: Optional[str] = None
    sku: Optional[str] = None
    status: Optional[ProductStatus] = None


class ProductUpdate(BaseModel):
    product_id: int
    category_id: Optional[int] = None
    nome: Optional[str] = None
    descricao: Optional[str] = None
    preco: Optional[float] = None
    preco_promocional: Optional[float] = None
    sku: Optional[str] = None
    quantidade_estoque: Optional[int] = None
    estoque_minimo: Optional[int] = None
    peso: Optional[float] = None
    dimensoes: Optional[str] = None
    status: Optional[ProductStatus] = None


class ProductResponse(BaseModel):
    id: int
    category_id: int
    nome: str
    descricao: Optional[str] = None
    preco: float
    preco_promocional: Optional[float] = None
    sku: str
    quantidade_estoque: int
    estoque_minimo: int
    peso: Optional[float] = None
    dimensoes: Optional[str] = None
    status: ProductStatus

    model_config = {"from_attributes": True}


class ProductListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    data: list[ProductResponse]
