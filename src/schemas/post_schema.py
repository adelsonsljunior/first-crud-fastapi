from pydantic import BaseModel
from datetime import datetime


class PostBase(BaseModel):
    username: str
    body: str


class PostCreateDto(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    archived: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class IdResponse(BaseModel):
    id: int
