from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db

from typing import List

from controllers.post_controller import PostController
from schemas.post_schema import PostCreateDto, PostResponse, IdResponse

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("", response_model=List[PostResponse])
async def find_all(db: Session = Depends(get_db)):
    controller = PostController(db)
    return controller.find_all()


@router.post("", response_model=IdResponse, status_code=201)
async def create(post: PostCreateDto, db: Session = Depends(get_db)):
    controller = PostController(db)
    return controller.create(post)
