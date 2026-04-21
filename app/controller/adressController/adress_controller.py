from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.model.userModel.user_model import UserModel
from app.schema.adressSchema.adress_schema import AdressCreate, AdressUpdate, AdressFilter, AdressResponse, AdressListResponse
from app.service.adressService import adress_service
from app.utils.auth import get_current_user

router = APIRouter(prefix="/adress", tags=["Adress"])


@router.post("/create", response_model=AdressResponse, status_code=status.HTTP_201_CREATED)
def create_adress(data: AdressCreate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    result, error = adress_service.create_adress(db, data, current_user.id)
    if error:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"status": "error", "message": error})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=result)


@router.post("/list", response_model=AdressListResponse)
def list_adresses(filters: AdressFilter, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    result, error = adress_service.get_adresses(db, filters)
    if error:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"status": "error", "message": error})
    return JSONResponse(status_code=status.HTTP_200_OK, content=result)


@router.put("/update", response_model=AdressResponse)
def update_adress(data: AdressUpdate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    result, error = adress_service.update_adress(db, data)
    if error:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"status": "error", "message": error})
    return JSONResponse(status_code=status.HTTP_200_OK, content=result)


@router.delete("/delete/{adress_id}", status_code=status.HTTP_200_OK)
def delete_adress(adress_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    result, error = adress_service.delete_adress(db, adress_id)
    if error:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"status": "error", "message": error})
    return JSONResponse(status_code=status.HTTP_200_OK, content=result)
