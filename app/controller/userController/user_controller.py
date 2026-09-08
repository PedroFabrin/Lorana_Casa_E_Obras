from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.schema.userSchema.user_schema import UserCreate, UserUpdate, UserFilter, UserResponse, UserListResponse
from app.service.userService import user_service
from app.utils.auth import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/create", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    result, error = user_service.create_user(db, data)
    if error:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"status": "error", "message": error})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=result)


@router.post("/list", response_model=UserListResponse)
def list_users(filters: UserFilter, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    result, error = user_service.get_users(db, filters, current_user)
    if error:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"status": "error", "message": error})
    return JSONResponse(status_code=status.HTTP_200_OK, content=result)



@router.put("/update", response_model=UserResponse)
def update_user(data: UserUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    result, error = user_service.update_user(db, data, current_user)
    if error:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"status": "error", "message": error})
    return JSONResponse(status_code=status.HTTP_200_OK, content=result)


@router.delete("/delete/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(user_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    result, error = user_service.delete_user(db, user_id, current_user)
    if error:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"status": "error", "message": error})
    return JSONResponse(status_code=status.HTTP_200_OK, content=result)

