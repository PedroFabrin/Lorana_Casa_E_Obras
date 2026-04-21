from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.schema.authSchema.auth_schema import LoginRequest
from app.service.authService import auth_service

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    result, error = auth_service.login(db, data)
    if error:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                            content={"status": "error", "message": error})
    return JSONResponse(status_code=status.HTTP_200_OK, content=result)
