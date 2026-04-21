from datetime import datetime
from sqlalchemy.orm import Session
from app.model.categoryModel.category_model import CategoryModel
from app.schema.categorySchema.category_schema import CategoryCreate, CategoryUpdate, CategoryFilter, CategoryResponse, CategoryListResponse


def create_category(db: Session, data: CategoryCreate):
    try:
        if db.query(CategoryModel).filter(CategoryModel.nome == data.nome, CategoryModel.deleted_at == None).first():
            return None, "Categoria já cadastrada com esse nome"

        category = CategoryModel(nome=data.nome, descricao=data.descricao)
        db.add(category)
        db.commit()
        db.refresh(category)

        result = CategoryResponse.model_validate(category)
        return {"status": "success", "data": result.model_dump()}, None
    except Exception as e:
        return None, str(e)


def get_category(db: Session, category_id: int):
    try:
        category = db.query(CategoryModel).filter(CategoryModel.id == category_id, CategoryModel.deleted_at == None).first()
        if not category:
            return None, "Categoria não encontrada"

        result = CategoryResponse.model_validate(category)
        return {"status": "success", "data": result.model_dump()}, None
    except Exception as e:
        return None, str(e)


def get_categories(db: Session, filters: CategoryFilter):
    try:
        query = db.query(CategoryModel).filter(CategoryModel.deleted_at == None)

        if filters.nome:
            query = query.filter(CategoryModel.nome.ilike(f"%{filters.nome}%"))

        total = query.count()
        offset = (filters.page - 1) * filters.page_size
        categories = query.offset(offset).limit(filters.page_size).all()

        result = CategoryListResponse(
            total=total,
            page=filters.page,
            page_size=filters.page_size,
            data=[CategoryResponse.model_validate(c) for c in categories],
        )
        return {"status": "success", "data": result.model_dump()}, None
    except Exception as e:
        return None, str(e)


def update_category(db: Session, data: CategoryUpdate):
    try:
        category = db.query(CategoryModel).filter(CategoryModel.id == data.category_id, CategoryModel.deleted_at == None).first()
        if not category:
            return None, "Categoria não encontrada"

        for field, value in data.model_dump(exclude_none=True, exclude={"category_id"}).items():
            setattr(category, field, value)

        db.commit()
        db.refresh(category)

        result = CategoryResponse.model_validate(category)
        return {"status": "success", "data": result.model_dump()}, None
    except Exception as e:
        return None, str(e)


def delete_category(db: Session, category_id: int):
    try:
        category = db.query(CategoryModel).filter(CategoryModel.id == category_id, CategoryModel.deleted_at == None).first()
        if not category:
            return None, "Categoria não encontrada"

        category.deleted_at = datetime.now()
        db.commit()
        return {"status": "success", "message": "Categoria deletada com sucesso"}, None
    except Exception as e:
        return None, str(e)
