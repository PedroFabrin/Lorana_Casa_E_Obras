from datetime import datetime
from sqlalchemy.orm import Session
from app.model.categoryModel.category_model import CategoryModel
from app.model.sectionModel.section_model import SectionModel
from app.model.productModel.product_model import ProductModel, ProductStatus
from app.schema.categorySchema.category_schema import CategoryCreate, CategoryUpdate, CategoryFilter, CategoryResponse, CategoryListResponse


def create_category(db: Session, data: CategoryCreate):
    try:
        if not db.query(SectionModel).filter(SectionModel.id == data.section_id, SectionModel.deleted_at == None).first():
            return None, "Seção não encontrada"

        if db.query(CategoryModel).filter(CategoryModel.nome == data.nome, CategoryModel.deleted_at == None).first():
            return None, "Categoria já cadastrada com esse nome"

        category = CategoryModel(section_id=data.section_id, nome=data.nome, descricao=data.descricao, status=data.status)
        db.add(category)
        db.commit()
        db.refresh(category)

        result = CategoryResponse.model_validate(category)
        return {"status": "success", "data": result.model_dump(mode='json')}, None
    except Exception as e:
        return None, str(e)


def get_category(db: Session, category_id: int):
    try:
        category = db.query(CategoryModel).filter(CategoryModel.id == category_id, CategoryModel.deleted_at == None).first()
        if not category:
            return None, "Categoria não encontrada"

        result = CategoryResponse.model_validate(category)
        return {"status": "success", "data": result.model_dump(mode='json')}, None
    except Exception as e:
        return None, str(e)


def get_categories(db: Session, filters: CategoryFilter):
    try:
        query = db.query(CategoryModel).filter(CategoryModel.deleted_at == None)

        if filters.section_id:
            query = query.filter(CategoryModel.section_id == filters.section_id)
        if filters.nome:
            query = query.filter(CategoryModel.nome.ilike(f"%{filters.nome}%"))
        if filters.status:
            query = query.filter(CategoryModel.status == filters.status)

        total = query.count()
        offset = (filters.page - 1) * filters.page_size
        categories = query.offset(offset).limit(filters.page_size).all()

        result = CategoryListResponse(
            total=total,
            page=filters.page,
            page_size=filters.page_size,
            data=[CategoryResponse.model_validate(c) for c in categories],
        )
        return {"status": "success", "data": result.model_dump(mode='json')}, None
    except Exception as e:
        return None, str(e)


def update_category(db: Session, data: CategoryUpdate):
    try:
        category = db.query(CategoryModel).filter(CategoryModel.id == data.category_id, CategoryModel.deleted_at == None).first()
        if not category:
            return None, "Categoria não encontrada"

        fields = data.model_dump(exclude_none=True, exclude={"category_id"})

        if "section_id" in fields:
            if not db.query(SectionModel).filter(SectionModel.id == fields["section_id"], SectionModel.deleted_at == None).first():
                return None, "Seção não encontrada"

        for field, value in fields.items():
            setattr(category, field, value)

        db.commit()
        db.refresh(category)

        result = CategoryResponse.model_validate(category)
        return {"status": "success", "data": result.model_dump(mode='json')}, None
    except Exception as e:
        return None, str(e)


def delete_category(db: Session, category_id: int):
    try:
        category = db.query(CategoryModel).filter(CategoryModel.id == category_id, CategoryModel.deleted_at == None).first()
        if not category:
            return None, "Categoria não encontrada"

        has_active_product = db.query(ProductModel).filter(
            ProductModel.category_id == category_id,
            ProductModel.status == ProductStatus.ativo,
            ProductModel.deleted_at == None,
        ).first()
        if has_active_product:
            return None, "Não é possível excluir a categoria: há produtos ativos vinculados"

        category.deleted_at = datetime.now()
        db.commit()
        return {"status": "success", "message": "Categoria deletada com sucesso"}, None
    except Exception as e:
        return None, str(e)
