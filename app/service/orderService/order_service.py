from datetime import datetime
from sqlalchemy.orm import Session
from app.model.adressModel.adress_model import AdressModel
from app.model.cartModel.cart_model import CartModel
from app.model.cartItemModel.cart_item_model import CartItemModel
from app.model.productModel.product_model import ProductModel, ProductStatus
from app.model.orderModel.order_model import OrderModel, OrderStatus
from app.model.orderItemModel.order_item_model import OrderItemModel
from app.model.paymentModel.payment_model import PaymentModel, PaymentStatus
from app.model.userModel.user_model import UserModel, UserRole
from app.schema.orderSchema.order_schema import (
    OrderCheckout, OrderFilter, OrderUpdateStatus,
    OrderItemResponse, PaymentResponse, OrderResponse, OrderListResponse,
)
from app.service.productService.product_service import get_effective_price
from app.service.paymentService import payment_service
from app.utils.email import send_email

ALLOWED_TRANSITIONS = {
    OrderStatus.pendente: {OrderStatus.cancelado},
    OrderStatus.pago: {OrderStatus.em_separacao, OrderStatus.cancelado},
    OrderStatus.em_separacao: {OrderStatus.enviado, OrderStatus.cancelado},
    OrderStatus.enviado: {OrderStatus.entregue, OrderStatus.cancelado},
    OrderStatus.entregue: set(),
    OrderStatus.cancelado: set(),
    OrderStatus.nao_aprovado: set(),
}

STOCK_DECREMENTED_STATUSES = {OrderStatus.pago, OrderStatus.em_separacao, OrderStatus.enviado}


def _build_order_response(order: OrderModel) -> OrderResponse:
    items = [
        OrderItemResponse(
            id=item.id,
            product_id=item.product_id,
            product_nome=item.product.nome,
            quantidade=item.quantidade,
            preco_unitario=float(item.preco_unitario),
            subtotal=float(item.subtotal),
        )
        for item in order.items
    ]
    payment = PaymentResponse.model_validate(order.payment) if order.payment else None
    return OrderResponse(
        id=order.id,
        user_id=order.user_id,
        adress_id=order.adress_id,
        status=order.status,
        subtotal=float(order.subtotal),
        desconto=float(order.desconto),
        total=float(order.total),
        created_at=order.created_at,
        items=items,
        payment=payment,
    )


def _notify_low_stock(db: Session, product: ProductModel):
    if product.quantidade_estoque >= product.estoque_minimo:
        return
    admins = db.query(UserModel).filter(UserModel.role == UserRole.admin, UserModel.deleted_at == None).all()
    for admin in admins:
        send_email(
            admin.email,
            "Alerta de estoque baixo",
            f"O produto '{product.nome}' (SKU {product.sku}) está com estoque de {product.quantidade_estoque} unidades, "
            f"abaixo do mínimo de {product.estoque_minimo}.",
        )


def _apply_payment_result(db: Session, order: OrderModel, payment: PaymentModel, payment_status: PaymentStatus):
    payment.status = payment_status

    if payment_status == PaymentStatus.aprovado:
        order.status = OrderStatus.pago
        for item in order.items:
            item.product.quantidade_estoque -= item.quantidade
            _notify_low_stock(db, item.product)
        db.commit()
        send_email(
            order.user.email,
            "Pedido confirmado",
            f"Seu pedido #{order.id} foi confirmado. Total: R$ {order.total}.",
        )
    elif payment_status == PaymentStatus.pendente:
        order.status = OrderStatus.pendente
        db.commit()
    else:
        order.status = OrderStatus.nao_aprovado
        db.commit()


def checkout(db: Session, user: UserModel, data: OrderCheckout):
    try:
        adress = db.query(AdressModel).filter(
            AdressModel.id == data.adress_id, AdressModel.user_id == user.id, AdressModel.deleted_at == None,
        ).first()
        if not adress:
            return None, "Endereço não encontrado"

        cart = db.query(CartModel).filter(CartModel.user_id == user.id, CartModel.deleted_at == None).first()
        cart_items = db.query(CartItemModel).filter(
            CartItemModel.cart_id == cart.id, CartItemModel.deleted_at == None,
        ).all() if cart else []
        if not cart_items:
            return None, "Carrinho vazio"

        for cart_item in cart_items:
            product = cart_item.product
            if product.status != ProductStatus.ativo:
                return None, f"Produto '{product.nome}' está indisponível"
            if cart_item.quantidade > product.quantidade_estoque:
                return None, f"Estoque insuficiente para o produto '{product.nome}'"

        subtotal_total = 0.0
        order_items_data = []
        for cart_item in cart_items:
            product = cart_item.product
            preco_unitario = get_effective_price(product)
            item_subtotal = round(preco_unitario * cart_item.quantidade, 2)
            subtotal_total += item_subtotal
            order_items_data.append((product, cart_item.quantidade, preco_unitario, item_subtotal))

        subtotal_total = round(subtotal_total, 2)

        order = OrderModel(user_id=user.id, adress_id=adress.id, subtotal=subtotal_total, total=subtotal_total)
        db.add(order)
        db.flush()

        for product, quantidade, preco_unitario, item_subtotal in order_items_data:
            db.add(OrderItemModel(
                order_id=order.id, product_id=product.id, quantidade=quantidade,
                preco_unitario=preco_unitario, subtotal=item_subtotal,
            ))

        payment = PaymentModel(order_id=order.id, forma_pagamento=data.forma_pagamento, valor=subtotal_total)
        db.add(payment)
        db.commit()
        db.refresh(order)

        gateway_name, payment_status, transaction_id = payment_service.process_payment(order, data.forma_pagamento)
        payment.gateway = gateway_name
        payment.transaction_id = transaction_id
        db.commit()

        _apply_payment_result(db, order, payment, payment_status)

        if payment_status != PaymentStatus.recusado:
            for cart_item in cart_items:
                cart_item.deleted_at = datetime.now()
            db.commit()

        db.refresh(order)
        result = _build_order_response(order)
        return {"status": "success", "data": result.model_dump(mode='json')}, None
    except Exception as e:
        return None, str(e)


def confirm_payment(db: Session, order_id: int, aprovado: bool):
    try:
        order = db.query(OrderModel).filter(OrderModel.id == order_id, OrderModel.deleted_at == None).first()
        if not order:
            return None, "Pedido não encontrado"
        if not order.payment or order.payment.status != PaymentStatus.pendente:
            return None, "Pagamento do pedido não está pendente"

        payment_status = PaymentStatus.aprovado if aprovado else PaymentStatus.recusado
        _apply_payment_result(db, order, order.payment, payment_status)

        db.refresh(order)
        result = _build_order_response(order)
        return {"status": "success", "data": result.model_dump(mode='json')}, None
    except Exception as e:
        return None, str(e)


def get_order(db: Session, order_id: int, current_user: UserModel):
    try:
        order = db.query(OrderModel).filter(OrderModel.id == order_id, OrderModel.deleted_at == None).first()
        if not order:
            return None, "Pedido não encontrado"
        if current_user.role != UserRole.admin and order.user_id != current_user.id:
            return None, "Acesso negado"

        result = _build_order_response(order)
        return {"status": "success", "data": result.model_dump(mode='json')}, None
    except Exception as e:
        return None, str(e)


def list_orders(db: Session, current_user: UserModel, filters: OrderFilter):
    try:
        query = db.query(OrderModel).filter(OrderModel.deleted_at == None)

        user_id = filters.user_id if current_user.role == UserRole.admin else current_user.id
        if user_id:
            query = query.filter(OrderModel.user_id == user_id)
        if filters.status:
            query = query.filter(OrderModel.status == filters.status)
        if filters.data_inicio:
            query = query.filter(OrderModel.created_at >= filters.data_inicio)
        if filters.data_fim:
            query = query.filter(OrderModel.created_at <= filters.data_fim)

        query = query.order_by(OrderModel.created_at.desc())

        total = query.count()
        offset = (filters.page - 1) * filters.page_size
        orders = query.offset(offset).limit(filters.page_size).all()

        result = OrderListResponse(
            total=total,
            page=filters.page,
            page_size=filters.page_size,
            data=[_build_order_response(o) for o in orders],
        )
        return {"status": "success", "data": result.model_dump(mode='json')}, None
    except Exception as e:
        return None, str(e)


def update_order_status(db: Session, data: OrderUpdateStatus):
    try:
        order = db.query(OrderModel).filter(OrderModel.id == data.order_id, OrderModel.deleted_at == None).first()
        if not order:
            return None, "Pedido não encontrado"

        allowed = ALLOWED_TRANSITIONS.get(order.status, set())
        if data.status not in allowed:
            return None, f"Transição de '{order.status.value}' para '{data.status.value}' não é permitida"

        if data.status == OrderStatus.cancelado and order.status in STOCK_DECREMENTED_STATUSES:
            for item in order.items:
                item.product.quantidade_estoque += item.quantidade

        order.status = data.status
        db.commit()
        db.refresh(order)

        result = _build_order_response(order)
        return {"status": "success", "data": result.model_dump(mode='json')}, None
    except Exception as e:
        return None, str(e)
