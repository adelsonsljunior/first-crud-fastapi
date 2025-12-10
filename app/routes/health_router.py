from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.configs.database import get_db
from app.controllers.health_controller import HealthController
from app.schemas.health_schema import HealthResponse


router = APIRouter(prefix="/health", tags=["health"])


@router.get(
    "",
    responses={
        200: {"model": HealthResponse},
        503: {"model": HealthResponse}
    }
)
async def healthchecker(db: Session = Depends(get_db)):
    controller = HealthController(db)
    return controller.healthchecker()
