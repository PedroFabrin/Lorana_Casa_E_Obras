from datetime import datetime
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse, StreamingResponse
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.schema.reportSchema.report_schema import SalesReportFilter, SalesReportResponse
from app.model.orderModel.order_model import OrderStatus
from app.service.reportService import report_service
from app.utils.auth import get_current_admin

router = APIRouter(prefix="/report", tags=["Report"])


@router.post("/sales", response_model=SalesReportResponse)
def get_sales_report(filters: SalesReportFilter, db: Session = Depends(get_db), current_user=Depends(get_current_admin)):
    result, error = report_service.get_sales_report(db, filters)
    if error:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"status": "error", "message": error})
    return JSONResponse(status_code=status.HTTP_200_OK, content=result)


@router.get("/sales/csv")
def export_sales_csv(
    data_inicio: Optional[datetime] = None,
    data_fim: Optional[datetime] = None,
    status_filtro: Optional[OrderStatus] = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin),
):
    filters = SalesReportFilter(data_inicio=data_inicio, data_fim=data_fim, status=status_filtro)
    csv_content = report_service.export_sales_csv(db, filters)
    return StreamingResponse(
        iter([csv_content]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=relatorio_vendas.csv"},
    )
