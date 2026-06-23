from datetime import datetime
from sqlalchemy.orm import Session
from app.model.sectionModel.section_model import SectionModel
from app.model.categoryModel.category_model import CategoryModel, CategoryStatus
from app.schema.sectionSchema.section_schema import SectionCreate, SectionUpdate, SectionFilter, SectionResponse, SectionListResponse


def create_section(db: Session, data: SectionCreate):
    try:
        if db.query(SectionModel).filter(SectionModel.nome == data.nome, SectionModel.deleted_at == None).first():
            return None, "Seção já cadastrada com esse nome"

        section = SectionModel(nome=data.nome, descricao=data.descricao, status=data.status)
        db.add(section)
        db.commit()
        db.refresh(section)

        result = SectionResponse.model_validate(section)
        return {"status": "success", "data": result.model_dump(mode='json')}, None
    except Exception as e:
        return None, str(e)


def get_section(db: Session, section_id: int):
    try:
        section = db.query(SectionModel).filter(SectionModel.id == section_id, SectionModel.deleted_at == None).first()
        if not section:
            return None, "Seção não encontrada"

        result = SectionResponse.model_validate(section)
        return {"status": "success", "data": result.model_dump(mode='json')}, None
    except Exception as e:
        return None, str(e)


def get_sections(db: Session, filters: SectionFilter):
    try:
        query = db.query(SectionModel).filter(SectionModel.deleted_at == None)

        if filters.nome:
            query = query.filter(SectionModel.nome.ilike(f"%{filters.nome}%"))
        if filters.status:
            query = query.filter(SectionModel.status == filters.status)

        total = query.count()
        offset = (filters.page - 1) * filters.page_size
        sections = query.offset(offset).limit(filters.page_size).all()

        result = SectionListResponse(
            total=total,
            page=filters.page,
            page_size=filters.page_size,
            data=[SectionResponse.model_validate(s) for s in sections],
        )
        return {"status": "success", "data": result.model_dump(mode='json')}, None
    except Exception as e:
        return None, str(e)


def update_section(db: Session, data: SectionUpdate):
    try:
        section = db.query(SectionModel).filter(SectionModel.id == data.section_id, SectionModel.deleted_at == None).first()
        if not section:
            return None, "Seção não encontrada"

        for field, value in data.model_dump(exclude_none=True, exclude={"section_id"}).items():
            setattr(section, field, value)

        db.commit()
        db.refresh(section)

        result = SectionResponse.model_validate(section)
        return {"status": "success", "data": result.model_dump(mode='json')}, None
    except Exception as e:
        return None, str(e)


def delete_section(db: Session, section_id: int):
    try:
        section = db.query(SectionModel).filter(SectionModel.id == section_id, SectionModel.deleted_at == None).first()
        if not section:
            return None, "Seção não encontrada"

        has_active_category = db.query(CategoryModel).filter(
            CategoryModel.section_id == section_id,
            CategoryModel.status == CategoryStatus.ativo,
            CategoryModel.deleted_at == None,
        ).first()
        if has_active_category:
            return None, "Não é possível excluir a seção: há categorias ativas vinculadas"

        section.deleted_at = datetime.now()
        db.commit()
        return {"status": "success", "message": "Seção deletada com sucesso"}, None
    except Exception as e:
        return None, str(e)
