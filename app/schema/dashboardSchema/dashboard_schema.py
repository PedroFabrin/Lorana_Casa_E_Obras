from pydantic import BaseModel


class LowStockProduct(BaseModel):
    id: int
    nome: str
    sku: str
    quantidade_estoque: int
    estoque_minimo: int


class DashboardResponse(BaseModel):
    faturamento_7_dias: float
    faturamento_30_dias: float
    pedidos_pendentes: int
    pedidos_pagos: int
    pedidos_enviados: int
    produtos_estoque_baixo: list[LowStockProduct]
    total_usuarios: int
