from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.schema.authSchema.auth_schema import LoginRequest
from app.service.authService import auth_service
from app.utils.auth import bearer_scheme, get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    result, error = auth_service.login(db, data)
    if error:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                            content={"status": "error", "message": error})
    return JSONResponse(status_code=status.HTTP_200_OK, content=result)


@router.post("/logout")
def logout(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result, error = auth_service.logout(db, credentials.credentials)
    if error:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"status": "error", "message": error})
    return JSONResponse(status_code=status.HTTP_200_OK, content=result)
