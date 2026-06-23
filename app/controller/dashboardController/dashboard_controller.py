from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.schema.dashboardSchema.dashboard_schema import DashboardResponse
from app.service.dashboardService import dashboard_service
from app.utils.auth import get_current_admin

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("", response_model=DashboardResponse)
def get_dashboard(db: Session = Depends(get_db), current_user=Depends(get_current_admin)):
    result, error = dashboard_service.get_dashboard(db)
    if error:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"status": "error", "message": error})
    return JSONResponse(status_code=status.HTTP_200_OK, content=result)
