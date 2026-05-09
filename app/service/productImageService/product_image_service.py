from datetime import datetime
from sqlalchemy.orm import Session
from app.model.productImageModel.product_image_model import ProductImageModel
from app.model.productModel.product_model import ProductModel
from app.schema.productImageSchema.product_image_schema import ProductImageCreate, ProductImageUpdate, ProductImageFilter, ProductImageResponse, ProductImageListResponse


def create_product_image(db: Session, data: ProductImageCreate):
    try:
        if not db.query(ProductModel).filter(ProductModel.id == data.product_id, ProductModel.deleted_at == None).first():
            return None, "Produto não encontrado"

        if data.principal:
            db.query(ProductImageModel).filter(
                ProductImageModel.product_id == data.product_id,
                ProductImageModel.deleted_at == None,
            ).update({"principal": False})

        image = ProductImageModel(
            product_id=data.product_id,
            url=data.url,
            principal=data.principal,
        )
        db.add(image)
        db.commit()
        db.refresh(image)

        result = ProductImageResponse.model_validate(image)
        return {"status": "success", "data": result.model_dump()}, None
    except Exception as e:
        return None, str(e)


def get_product_image(db: Session, product_image_id: int):
    try:
        image = db.query(ProductImageModel).filter(ProductImageModel.id == product_image_id, ProductImageModel.deleted_at == None).first()
        if not image:
            return None, "Imagem não encontrada"

        result = ProductImageResponse.model_validate(image)
        return {"status": "success", "data": result.model_dump()}, None
    except Exception as e:
        return None, str(e)


def get_product_images(db: Session, filters: ProductImageFilter):
    try:
        query = db.query(ProductImageModel).filter(ProductImageModel.deleted_at == None)

        if filters.product_id:
            query = query.filter(ProductImageModel.product_id == filters.product_id)
        if filters.principal is not None:
            query = query.filter(ProductImageModel.principal == filters.principal)

        total = query.count()
        offset = (filters.page - 1) * filters.page_size
        images = query.offset(offset).limit(filters.page_size).all()

        result = ProductImageListResponse(
            total=total,
            page=filters.page,
            page_size=filters.page_size,
            data=[ProductImageResponse.model_validate(i) for i in images],
        )
        return {"status": "success", "data": result.model_dump()}, None
    except Exception as e:
        return None, str(e)


def update_product_image(db: Session, data: ProductImageUpdate):
    try:
        image = db.query(ProductImageModel).filter(ProductImageModel.id == data.product_image_id, ProductImageModel.deleted_at == None).first()
        if not image:
            return None, "Imagem não encontrada"

        if data.principal:
            db.query(ProductImageModel).filter(
                ProductImageModel.product_id == image.product_id,
                ProductImageModel.deleted_at == None,
            ).update({"principal": False})

        fields = data.model_dump(exclude_none=True, exclude={"product_image_id"})
        for field, value in fields.items():
            setattr(image, field, value)

        db.commit()
        db.refresh(image)

        result = ProductImageResponse.model_validate(image)
        return {"status": "success", "data": result.model_dump()}, None
    except Exception as e:
        return None, str(e)


def delete_product_image(db: Session, product_image_id: int):
    try:
        image = db.query(ProductImageModel).filter(ProductImageModel.id == product_image_id, ProductImageModel.deleted_at == None).first()
        if not image:
            return None, "Imagem não encontrada"

        image.deleted_at = datetime.now()
        db.commit()
        return {"status": "success", "message": "Imagem deletada com sucesso"}, None
    except Exception as e:
        return None, str(e)
