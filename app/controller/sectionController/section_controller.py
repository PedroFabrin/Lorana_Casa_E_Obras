from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.schema.sectionSchema.section_schema import SectionCreate, SectionUpdate, SectionFilter, SectionResponse, SectionListResponse
from app.service.sectionService import section_service
from app.utils.auth import get_current_user, get_current_admin

router = APIRouter(prefix="/section", tags=["Section"])


@router.post("/create", response_model=SectionResponse, status_code=status.HTTP_201_CREATED)
def create_section(data: SectionCreate, db: Session = Depends(get_db), current_user=Depends(get_current_admin)):
    result, error = section_service.create_section(db, data)
    if error:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"status": "error", "message": error})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=result)


@router.post("/list", response_model=SectionListResponse)
def list_sections(filters: SectionFilter, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    result, error = section_service.get_sections(db, filters)
    if error:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"status": "error", "message": error})
    return JSONResponse(status_code=status.HTTP_200_OK, content=result)


@router.get("/{section_id}", response_model=SectionResponse)
def get_section(section_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    result, error = section_service.get_section(db, section_id)
    if error:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"status": "error", "message": error})
    return JSONResponse(status_code=status.HTTP_200_OK, content=result)


@router.put("/update", response_model=SectionResponse)
def update_section(data: SectionUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_admin)):
    result, error = section_service.update_section(db, data)
    if error:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"status": "error", "message": error})
    return JSONResponse(status_code=status.HTTP_200_OK, content=result)


@router.delete("/delete/{section_id}", status_code=status.HTTP_200_OK)
def delete_section(section_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_admin)):
    result, error = section_service.delete_section(db, section_id)
    if error:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"status": "error", "message": error})
    return JSONResponse(status_code=status.HTTP_200_OK, content=result)
