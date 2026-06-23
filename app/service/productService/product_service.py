from datetime import datetime
from sqlalchemy.orm import Session
from app.model.productModel.product_model import ProductModel
from app.model.categoryModel.category_model import CategoryModel
from app.schema.productSchema.product_schema import ProductCreate, ProductUpdate, ProductFilter, ProductResponse, ProductListResponse


def get_effective_price(product: ProductModel) -> float:
    if product.preco_promocional is not None and product.preco_promocional < product.preco:
        return float(product.preco_promocional)
    return float(product.preco)


def create_product(db: Session, data: ProductCreate):
    try:
        if not db.query(CategoryModel).filter(CategoryModel.id == data.category_id, CategoryModel.deleted_at == None).first():
            return None, "Categoria não encontrada"

        if db.query(ProductModel).filter(ProductModel.sku == data.sku, ProductModel.deleted_at == None).first():
            return None, "SKU já cadastrado"

        if data.preco_promocional is not None and data.preco_promocional >= data.preco:
            return None, "Preço promocional deve ser menor que o preço normal"

        product = ProductModel(
            category_id=data.category_id,
            nome=data.nome,
            descricao=data.descricao,
            preco=data.preco,
            preco_promocional=data.preco_promocional,
            sku=data.sku,
            quantidade_estoque=data.quantidade_estoque,
            estoque_minimo=data.estoque_minimo,
            peso=data.peso,
            dimensoes=data.dimensoes,
            status=data.status,
        )
        db.add(product)
        db.commit()
        db.refresh(product)

        result = ProductResponse.model_validate(product)
        return {"status": "success", "data": result.model_dump(mode='json')}, None
    except Exception as e:
        return None, str(e)


def get_product(db: Session, product_id: int):
    try:
        product = db.query(ProductModel).filter(ProductModel.id == product_id, ProductModel.deleted_at == None).first()
        if not product:
            return None, "Produto não encontrado"

        result = ProductResponse.model_validate(product)
        return {"status": "success", "data": result.model_dump(mode='json')}, None
    except Exception as e:
        return None, str(e)


def get_products(db: Session, filters: ProductFilter):
    try:
        query = db.query(ProductModel).filter(ProductModel.deleted_at == None)

        if filters.category_id:
            query = query.filter(ProductModel.category_id == filters.category_id)
        if filters.nome:
            query = query.filter(ProductModel.nome.ilike(f"%{filters.nome}%"))
        if filters.sku:
            query = query.filter(ProductModel.sku == filters.sku)
        if filters.status:
            query = query.filter(ProductModel.status == filters.status)

        total = query.count()
        offset = (filters.page - 1) * filters.page_size
        products = query.offset(offset).limit(filters.page_size).all()

        result = ProductListResponse(
            total=total,
            page=filters.page,
            page_size=filters.page_size,
            data=[ProductResponse.model_validate(p) for p in products],
        )
        return {"status": "success", "data": result.model_dump(mode='json')}, None
    except Exception as e:
        return None, str(e)


def update_product(db: Session, data: ProductUpdate):
    try:
        product = db.query(ProductModel).filter(ProductModel.id == data.product_id, ProductModel.deleted_at == None).first()
        if not product:
            return None, "Produto não encontrado"

        fields = data.model_dump(exclude_none=True, exclude={"product_id"})

        if "sku" in fields and fields["sku"] != product.sku:
            if db.query(ProductModel).filter(ProductModel.sku == fields["sku"], ProductModel.deleted_at == None).first():
                return None, "SKU já cadastrado"

        preco = fields.get("preco", float(product.preco))
        preco_promocional = fields.get("preco_promocional", float(product.preco_promocional) if product.preco_promocional else None)
        if preco_promocional is not None and preco_promocional >= preco:
            return None, "Preço promocional deve ser menor que o preço normal"

        for field, value in fields.items():
            setattr(product, field, value)

        db.commit()
        db.refresh(product)

        result = ProductResponse.model_validate(product)
        return {"status": "success", "data": result.model_dump(mode='json')}, None
    except Exception as e:
        return None, str(e)


def delete_product(db: Session, product_id: int):
    try:
        product = db.query(ProductModel).filter(ProductModel.id == product_id, ProductModel.deleted_at == None).first()
        if not product:
            return None, "Produto não encontrado"

        product.deleted_at = datetime.now()
        db.commit()
        return {"status": "success", "message": "Produto deletado com sucesso"}, None
    except Exception as e:
        return None, str(e)
