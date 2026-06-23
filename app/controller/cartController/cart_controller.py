from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.schema.cartSchema.cart_schema import CartItemAdd, CartItemUpdate
from app.service.cartService import cart_service
from app.utils.auth import get_current_user

router = APIRouter(prefix="/cart", tags=["Cart"])


@router.get("", status_code=status.HTTP_200_OK)
def get_cart(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    result, error = cart_service.get_cart(db, current_user)
    if error:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"status": "error", "message": error})
    return JSONResponse(status_code=status.HTTP_200_OK, content=result)


@router.post("/add", status_code=status.HTTP_200_OK)
def add_item(data: CartItemAdd, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    result, error = cart_service.add_item(db, current_user, data)
    if error:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"status": "error", "message": error})
    return JSONResponse(status_code=status.HTTP_200_OK, content=result)


@router.put("/update-item", status_code=status.HTTP_200_OK)
def update_item(data: CartItemUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    result, error = cart_service.update_item(db, current_user, data)
    if error:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"status": "error", "message": error})
    return JSONResponse(status_code=status.HTTP_200_OK, content=result)


@router.delete("/remove-item/{cart_item_id}", status_code=status.HTTP_200_OK)
def remove_item(cart_item_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    result, error = cart_service.remove_item(db, current_user, cart_item_id)
    if error:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"status": "error", "message": error})
    return JSONResponse(status_code=status.HTTP_200_OK, content=result)


@router.delete("/clear", status_code=status.HTTP_200_OK)
def clear_cart(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    result, error = cart_service.clear_cart(db, current_user)
    if error:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"status": "error", "message": error})
    return JSONResponse(status_code=status.HTTP_200_OK, content=result)
