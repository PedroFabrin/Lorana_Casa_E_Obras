from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users/types", tags=["UsersTypes"])

@router.post("/create")
def create_user():
    return None

@router.post("/list")
def list_users():
    return None

@router.put("/update")
def update_user():
    return None

@router.delete("/delete/{user_id}")
def delete_user():
    return None

