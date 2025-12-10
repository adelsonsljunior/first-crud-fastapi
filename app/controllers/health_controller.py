from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import status
from fastapi.responses import JSONResponse

from app.schemas.health_schema import HealthResponse

class HealthController:
    def __init__(self, db: Session):
        self.db = db

    def healthchecker(self) -> HealthResponse:
        try:
            # Testa a conexão executando uma query simples
            self.db.execute(text("SELECT 1"))

            response = HealthResponse(status="ok", message="Postgres databse está on")
            return JSONResponse(
                content=response.model_dump()
            )

        except Exception as e:
            response = HealthResponse(status="failure", message="Postgres databse está off")
            return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                content=response.model_dump()
            )
