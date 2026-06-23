from pydantic import BaseModel
from typing import Optional
from app.schema.pagination import PaginationParams
from app.model.sectionModel.section_model import SectionStatus


class SectionCreate(BaseModel):
    nome: str
    descricao: Optional[str] = None
    status: SectionStatus = SectionStatus.ativo


class SectionFilter(PaginationParams):
    nome: Optional[str] = None
    status: Optional[SectionStatus] = None


class SectionUpdate(BaseModel):
    section_id: int
    nome: Optional[str] = None
    descricao: Optional[str] = None
    status: Optional[SectionStatus] = None


class SectionResponse(BaseModel):
    id: int
    nome: str
    descricao: Optional[str] = None
    status: SectionStatus

    model_config = {"from_attributes": True}


class SectionListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    data: list[SectionResponse]
