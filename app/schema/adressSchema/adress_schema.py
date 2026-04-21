from pydantic import BaseModel
from typing import Optional
from app.schema.pagination import PaginationParams


class AdressCreate(BaseModel):
    rua: str
    numero: str
    cep: str
    cidade: str
    uf: str


class AdressFilter(PaginationParams):
    user_id: Optional[int] = None
    cidade: Optional[str] = None
    uf: Optional[str] = None
    cep: Optional[str] = None


class AdressUpdate(BaseModel):
    adress_id: int
    rua: Optional[str] = None
    numero: Optional[str] = None
    cep: Optional[str] = None
    cidade: Optional[str] = None
    uf: Optional[str] = None


class AdressResponse(BaseModel):
    id: int
    user_id: int
    rua: str
    numero: str
    cep: str
    cidade: str
    uf: str

    model_config = {"from_attributes": True}


class AdressListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    data: list[AdressResponse]
