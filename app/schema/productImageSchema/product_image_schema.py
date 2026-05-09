from pydantic import BaseModel
from typing import Optional
from app.schema.pagination import PaginationParams


class ProductImageCreate(BaseModel):
    product_id: int
    url: str
    principal: bool = False


class ProductImageFilter(PaginationParams):
    product_id: Optional[int] = None
    principal: Optional[bool] = None


class ProductImageUpdate(BaseModel):
    product_image_id: int
    url: Optional[str] = None
    principal: Optional[bool] = None


class ProductImageResponse(BaseModel):
    id: int
    product_id: int
    url: str
    principal: bool

    model_config = {"from_attributes": True}


class ProductImageListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    data: list[ProductImageResponse]
