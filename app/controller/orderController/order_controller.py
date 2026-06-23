from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.schema.orderSchema.order_schema import OrderCheckout, OrderFilter, OrderUpdateStatus, OrderConfirmPayment, OrderResponse, OrderListResponse
from app.service.orderService import order_service
from app.utils.auth import get_current_user, get_current_admin

router = APIRouter(prefix="/order", tags=["Order"])


@router.post("/checkout", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def checkout(data: OrderCheckout, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    result, error = order_service.checkout(db, current_user, data)
    if error:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"status": "error", "message": error})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=result)


@router.post("/list", response_model=OrderListResponse)
def list_orders(filters: OrderFilter, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    result, error = order_service.list_orders(db, current_user, filters)
    if error:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"status": "error", "message": error})
    return JSONResponse(status_code=status.HTTP_200_OK, content=result)


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    result, error = order_service.get_order(db, order_id, current_user)
    if error:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"status": "error", "message": error})
    return JSONResponse(status_code=status.HTTP_200_OK, content=result)


@router.put("/update-status", response_model=OrderResponse)
def update_order_status(data: OrderUpdateStatus, db: Session = Depends(get_db), current_user=Depends(get_current_admin)):
    result, error = order_service.update_order_status(db, data)
    if error:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"status": "error", "message": error})
    return JSONResponse(status_code=status.HTTP_200_OK, content=result)


@router.post("/{order_id}/confirm-payment", response_model=OrderResponse)
def confirm_payment(order_id: int, data: OrderConfirmPayment, db: Session = Depends(get_db), current_user=Depends(get_current_admin)):
    result, error = order_service.confirm_payment(db, order_id, data.aprovado)
    if error:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"status": "error", "message": error})
    return JSONResponse(status_code=status.HTTP_200_OK, content=result)
