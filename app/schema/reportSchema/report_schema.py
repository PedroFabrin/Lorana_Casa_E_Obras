from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from app.model.orderModel.order_model import OrderStatus


class SalesReportFilter(BaseModel):
    data_inicio: Optional[datetime] = None
    data_fim: Optional[datetime] = None
    status: Optional[OrderStatus] = None


class SalesReportOrderItem(BaseModel):
    order_id: int
    data: datetime
    cliente: str
    total: float


class ProductSold(BaseModel):
    product_id: int
    nome: str
    quantidade_vendida: int


class SalesReportResponse(BaseModel):
    pedidos: list[SalesReportOrderItem]
    total_faturado: float
    produtos_mais_vendidos: list[ProductSold]
