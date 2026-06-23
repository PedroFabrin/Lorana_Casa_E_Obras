from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.schema.productImageSchema.product_image_schema import ProductImageCreate, ProductImageUpdate, ProductImageFilter
from app.service.productImageService import product_image_service
from app.utils.auth import get_current_user, get_current_admin

router = APIRouter(prefix="/product-image", tags=["ProductImage"])


@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_product_image(data: ProductImageCreate, db: Session = Depends(get_db), current_user=Depends(get_current_admin)):
    result, error = product_image_service.create_product_image(db, data)
    if error:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"status": "error", "message": error})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=result)


@router.post("/list", status_code=status.HTTP_200_OK)
def list_product_images(filters: ProductImageFilter, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    result, error = product_image_service.get_product_images(db, filters)
    if error:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"status": "error", "message": error})
    return JSONResponse(status_code=status.HTTP_200_OK, content=result)


@router.put("/update", status_code=status.HTTP_200_OK)
def update_product_image(data: ProductImageUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_admin)):
    result, error = product_image_service.update_product_image(db, data)
    if error:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"status": "error", "message": error})
    return JSONResponse(status_code=status.HTTP_200_OK, content=result)


@router.delete("/delete/{product_image_id}", status_code=status.HTTP_200_OK)
def delete_product_image(product_image_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_admin)):
    result, error = product_image_service.delete_product_image(db, product_image_id)
    if error:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"status": "error", "message": error})
    return JSONResponse(status_code=status.HTTP_200_OK, content=result)
