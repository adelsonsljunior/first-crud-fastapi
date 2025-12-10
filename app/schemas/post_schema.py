from pydantic import BaseModel, Field
from datetime import datetime


class PostBase(BaseModel):
    body: str = Field(
        min_length=1,
        max_length=255,
        description="O body deve ter entre 1 e 255 caracteres",
    )


class PostCreateDto(PostBase):
    username: str = Field(
        min_length=3,
        max_length=50,
        description="O username deve ter entre 3 e 50 caracteres",
    )


class PostUpdateDto(PostBase):
    pass


class PostResponseDto(PostBase):
    id: int
    username: str
    archived: bool
    created_at: datetime
    updated_at: datetime
