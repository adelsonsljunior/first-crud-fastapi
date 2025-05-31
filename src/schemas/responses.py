from pydantic import BaseModel


class IdResponse(BaseModel):
    id: int


class ErrorResponse(BaseModel):
    message: str
