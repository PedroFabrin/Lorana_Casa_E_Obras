from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.schema.categorySchema.category_schema import CategoryCreate, CategoryUpdate, CategoryFilter, CategoryResponse, CategoryListResponse
from app.service.categoryService import category_service
from app.utils.auth import get_current_admin

router = APIRouter(prefix="/category", tags=["Category"])


@router.post("/create", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(data: CategoryCreate, db: Session = Depends(get_db), current_user=Depends(get_current_admin)):
    result, error = category_service.create_category(db, data)
    if error:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"status": "error", "message": error})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=result)


@router.post("/list", response_model=CategoryListResponse)
def list_categories(filters: CategoryFilter, db: Session = Depends(get_db)):
    result, error = category_service.get_categories(db, filters)
    if error:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"status": "error", "message": error})
    return JSONResponse(status_code=status.HTTP_200_OK, content=result)


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    result, error = category_service.get_category(db, category_id)
    if error:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"status": "error", "message": error})
    return JSONResponse(status_code=status.HTTP_200_OK, content=result)


@router.put("/update", response_model=CategoryResponse)
def update_category(data: CategoryUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_admin)):
    result, error = category_service.update_category(db, data)
    if error:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"status": "error", "message": error})
    return JSONResponse(status_code=status.HTTP_200_OK, content=result)


@router.delete("/delete/{category_id}", status_code=status.HTTP_200_OK)
def delete_category(category_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_admin)):
    result, error = category_service.delete_category(db, category_id)
    if error:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"status": "error", "message": error})
    return JSONResponse(status_code=status.HTTP_200_OK, content=result)
