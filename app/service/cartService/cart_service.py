from datetime import datetime
from sqlalchemy.orm import Session
from app.model.cartModel.cart_model import CartModel
from app.model.cartItemModel.cart_item_model import CartItemModel
from app.model.productModel.product_model import ProductModel, ProductStatus
from app.model.userModel.user_model import UserModel
from app.schema.cartSchema.cart_schema import CartItemAdd, CartItemUpdate, CartItemResponse, CartResponse
from app.service.productService.product_service import get_effective_price


def _get_or_create_cart(db: Session, user: UserModel) -> CartModel:
    cart = db.query(CartModel).filter(CartModel.user_id == user.id, CartModel.deleted_at == None).first()
    if not cart:
        cart = CartModel(user_id=user.id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return cart


def _build_cart_response(db: Session, cart: CartModel):
    items = db.query(CartItemModel).filter(CartItemModel.cart_id == cart.id, CartItemModel.deleted_at == None).all()

    item_responses = []
    total = 0.0
    for item in items:
        preco_unitario = get_effective_price(item.product)
        subtotal = round(preco_unitario * item.quantidade, 2)
        total += subtotal
        item_responses.append(CartItemResponse(
            id=item.id,
            product_id=item.product_id,
            product_nome=item.product.nome,
            quantidade=item.quantidade,
            preco_unitario=preco_unitario,
            subtotal=subtotal,
        ))

    return CartResponse(id=cart.id, items=item_responses, total=round(total, 2))


def get_cart(db: Session, user: UserModel):
    try:
        cart = _get_or_create_cart(db, user)
        result = _build_cart_response(db, cart)
        return {"status": "success", "data": result.model_dump(mode='json')}, None
    except Exception as e:
        return None, str(e)


def add_item(db: Session, user: UserModel, data: CartItemAdd):
    try:
        product = db.query(ProductModel).filter(ProductModel.id == data.product_id, ProductModel.deleted_at == None).first()
        if not product:
            return None, "Produto não encontrado"
        if product.status != ProductStatus.ativo:
            return None, "Produto indisponível"

        cart = _get_or_create_cart(db, user)
        item = db.query(CartItemModel).filter(
            CartItemModel.cart_id == cart.id,
            CartItemModel.product_id == data.product_id,
            CartItemModel.deleted_at == None,
        ).first()

        nova_quantidade = data.quantidade + (item.quantidade if item else 0)
        if nova_quantidade <= 0:
            return None, "Quantidade deve ser maior que zero"
        if nova_quantidade > product.quantidade_estoque:
            return None, "Quantidade solicitada maior que o estoque disponível"

        if item:
            item.quantidade = nova_quantidade
        else:
            item = CartItemModel(cart_id=cart.id, product_id=data.product_id, quantidade=nova_quantidade)
            db.add(item)

        db.commit()

        result = _build_cart_response(db, cart)
        return {"status": "success", "data": result.model_dump(mode='json')}, None
    except Exception as e:
        return None, str(e)


def update_item(db: Session, user: UserModel, data: CartItemUpdate):
    try:
        cart = _get_or_create_cart(db, user)
        item = db.query(CartItemModel).filter(
            CartItemModel.id == data.cart_item_id,
            CartItemModel.cart_id == cart.id,
            CartItemModel.deleted_at == None,
        ).first()
        if not item:
            return None, "Item não encontrado no carrinho"

        if data.quantidade <= 0:
            return None, "Quantidade deve ser maior que zero"
        if data.quantidade > item.product.quantidade_estoque:
            return None, "Quantidade solicitada maior que o estoque disponível"

        item.quantidade = data.quantidade
        db.commit()

        result = _build_cart_response(db, cart)
        return {"status": "success", "data": result.model_dump(mode='json')}, None
    except Exception as e:
        return None, str(e)


def remove_item(db: Session, user: UserModel, cart_item_id: int):
    try:
        cart = _get_or_create_cart(db, user)
        item = db.query(CartItemModel).filter(
            CartItemModel.id == cart_item_id,
            CartItemModel.cart_id == cart.id,
            CartItemModel.deleted_at == None,
        ).first()
        if not item:
            return None, "Item não encontrado no carrinho"

        item.deleted_at = datetime.now()
        db.commit()

        result = _build_cart_response(db, cart)
        return {"status": "success", "data": result.model_dump(mode='json')}, None
    except Exception as e:
        return None, str(e)


def clear_cart(db: Session, user: UserModel):
    try:
        cart = _get_or_create_cart(db, user)
        db.query(CartItemModel).filter(
            CartItemModel.cart_id == cart.id,
            CartItemModel.deleted_at == None,
        ).update({CartItemModel.deleted_at: datetime.now()})
        db.commit()
        return {"status": "success", "message": "Carrinho esvaziado com sucesso"}, None
    except Exception as e:
        return None, str(e)
