from pydantic import BaseModel
from datetime import datetime


class PostBase(BaseModel):
    body: str


class PostCreateDto(PostBase):
    username: str | None


class PostUpdateDto(PostBase):
    pass


class PostResponseDto(PostBase):
    id: int
    username: str
    archived: bool
    created_at: datetime
    updated_at: datetime
