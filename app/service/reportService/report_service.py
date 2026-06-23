import csv
import io
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.model.orderModel.order_model import OrderModel, OrderStatus
from app.model.orderItemModel.order_item_model import OrderItemModel
from app.model.productModel.product_model import ProductModel
from app.schema.reportSchema.report_schema import SalesReportFilter, SalesReportOrderItem, ProductSold, SalesReportResponse

EXCLUDED_FROM_REVENUE = {OrderStatus.pendente, OrderStatus.cancelado, OrderStatus.nao_aprovado}


def _filtered_orders(db: Session, filters: SalesReportFilter):
    query = db.query(OrderModel).filter(OrderModel.deleted_at == None)

    if filters.data_inicio:
        query = query.filter(OrderModel.created_at >= filters.data_inicio)
    if filters.data_fim:
        query = query.filter(OrderModel.created_at <= filters.data_fim)
    if filters.status:
        query = query.filter(OrderModel.status == filters.status)
    else:
        query = query.filter(OrderModel.status.notin_(EXCLUDED_FROM_REVENUE))

    return query.order_by(OrderModel.created_at.desc()).all()


def get_sales_report(db: Session, filters: SalesReportFilter):
    try:
        orders = _filtered_orders(db, filters)

        pedidos = [
            SalesReportOrderItem(order_id=o.id, data=o.created_at, cliente=o.user.name, total=float(o.total))
            for o in orders
        ]
        total_faturado = round(sum(p.total for p in pedidos), 2)

        produtos_mais_vendidos = []
        order_ids = [o.id for o in orders]
        if order_ids:
            rows = (
                db.query(OrderItemModel.product_id, ProductModel.nome, func.sum(OrderItemModel.quantidade).label("qtd"))
                .join(ProductModel, ProductModel.id == OrderItemModel.product_id)
                .filter(OrderItemModel.order_id.in_(order_ids))
                .group_by(OrderItemModel.product_id, ProductModel.nome)
                .order_by(func.sum(OrderItemModel.quantidade).desc())
                .limit(10)
                .all()
            )
            produtos_mais_vendidos = [ProductSold(product_id=r[0], nome=r[1], quantidade_vendida=int(r[2])) for r in rows]

        result = SalesReportResponse(pedidos=pedidos, total_faturado=total_faturado, produtos_mais_vendidos=produtos_mais_vendidos)
        return {"status": "success", "data": result.model_dump(mode='json')}, None
    except Exception as e:
        return None, str(e)


def export_sales_csv(db: Session, filters: SalesReportFilter) -> str:
    orders = _filtered_orders(db, filters)

    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["pedido", "data", "cliente", "status", "total"])
    for o in orders:
        writer.writerow([o.id, o.created_at.isoformat(), o.user.name, o.status.value, float(o.total)])

    return buffer.getvalue()
