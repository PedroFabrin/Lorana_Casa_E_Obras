from datetime import datetime, timedelta
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.model.orderModel.order_model import OrderModel, OrderStatus
from app.model.productModel.product_model import ProductModel
from app.model.userModel.user_model import UserModel
from app.schema.dashboardSchema.dashboard_schema import LowStockProduct, DashboardResponse

REVENUE_STATUSES = [OrderStatus.pago, OrderStatus.em_separacao, OrderStatus.enviado, OrderStatus.entregue]


def _faturamento_desde(db: Session, dias: int) -> float:
    inicio = datetime.now() - timedelta(days=dias)
    total = db.query(func.sum(OrderModel.total)).filter(
        OrderModel.created_at >= inicio,
        OrderModel.status.in_(REVENUE_STATUSES),
        OrderModel.deleted_at == None,
    ).scalar()
    return float(total) if total else 0.0


def get_dashboard(db: Session):
    try:
        faturamento_7_dias = _faturamento_desde(db, 7)
        faturamento_30_dias = _faturamento_desde(db, 30)

        pedidos_pendentes = db.query(OrderModel).filter(
            OrderModel.status == OrderStatus.pendente, OrderModel.deleted_at == None,
        ).count()
        pedidos_pagos = db.query(OrderModel).filter(
            OrderModel.status == OrderStatus.pago, OrderModel.deleted_at == None,
        ).count()
        pedidos_enviados = db.query(OrderModel).filter(
            OrderModel.status == OrderStatus.enviado, OrderModel.deleted_at == None,
        ).count()

        low_stock_products = db.query(ProductModel).filter(
            ProductModel.quantidade_estoque < ProductModel.estoque_minimo,
            ProductModel.deleted_at == None,
        ).all()
        produtos_estoque_baixo = [
            LowStockProduct(id=p.id, nome=p.nome, sku=p.sku, quantidade_estoque=p.quantidade_estoque, estoque_minimo=p.estoque_minimo)
            for p in low_stock_products
        ]

        total_usuarios = db.query(UserModel).filter(UserModel.deleted_at == None).count()

        result = DashboardResponse(
            faturamento_7_dias=faturamento_7_dias,
            faturamento_30_dias=faturamento_30_dias,
            pedidos_pendentes=pedidos_pendentes,
            pedidos_pagos=pedidos_pagos,
            pedidos_enviados=pedidos_enviados,
            produtos_estoque_baixo=produtos_estoque_baixo,
            total_usuarios=total_usuarios,
        )
        return {"status": "success", "data": result.model_dump(mode='json')}, None
    except Exception as e:
        return None, str(e)
