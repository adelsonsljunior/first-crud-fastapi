from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from typing import List

from database import get_db
from controllers.post_controller import PostController
from schemas.post_schema import PostCreateDto, PostResponse
from schemas.responses import IdResponse, ErrorResponse

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("", response_model=List[PostResponse])
async def find_all(db: Session = Depends(get_db)):
    controller = PostController(db)
    return controller.find_all()


@router.post("", response_model=IdResponse, status_code=201)
async def create(post: PostCreateDto, db: Session = Depends(get_db)):
    controller = PostController(db)
    return controller.create(post)


@router.get(
    "/{post_id}", response_model=PostResponse, responses={404: {"model": ErrorResponse}}
)
async def find_by_id(post_id: int, db: Session = Depends(get_db)):
    controller = PostController(db)
    return controller.find_by_id(post_id)
