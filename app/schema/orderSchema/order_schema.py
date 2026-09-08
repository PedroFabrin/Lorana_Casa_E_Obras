from datetime import datetime
from pydantic import BaseModel
from typing import Optional, Literal
from app.schema.pagination import PaginationParams
from app.model.orderModel.order_model import OrderStatus
from app.model.paymentModel.payment_model import PaymentGatewayEnum, PaymentStatus


class OrderCheckout(BaseModel):
    adress_id: int
    forma_pagamento: Literal["cartao", "boleto", "pix"]


class OrderFilter(PaginationParams):
    user_id: Optional[int] = None
    status: Optional[OrderStatus] = None
    data_inicio: Optional[datetime] = None
    data_fim: Optional[datetime] = None


class OrderUpdateStatus(BaseModel):
    order_id: int
    status: OrderStatus


class OrderConfirmPayment(BaseModel):
    aprovado: bool = True


class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    product_nome: str
    quantidade: int
    preco_unitario: float
    subtotal: float

    model_config = {"from_attributes": True}


class PaymentResponse(BaseModel):
    id: int
    gateway: PaymentGatewayEnum
    forma_pagamento: str
    status: PaymentStatus
    transaction_id: Optional[str] = None
    valor: float

    model_config = {"from_attributes": True}


class OrderResponse(BaseModel):
    id: int
    user_id: int
    adress_id: int
    status: OrderStatus
    subtotal: float
    desconto: float
    total: float
    created_at: datetime
    items: list[OrderItemResponse]
    payment: Optional[PaymentResponse] = None
    checkout_url: Optional[str] = None

    model_config = {"from_attributes": True}


class OrderListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    data: list[OrderResponse]
