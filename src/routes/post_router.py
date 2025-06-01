from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from typing import List

from database import get_db
from controllers.post_controller import PostController
from schemas.post_schema import PostCreateDto, PostResponseDto, PostUpdateDto
from schemas.responses import IdResponse, ErrorResponse, PaginationResponse

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("", response_model=PaginationResponse[PostResponseDto])
async def find_all(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1),
    db: Session = Depends(get_db),
):
    controller = PostController(db)
    return controller.find_all(page, limit)


@router.post("", response_model=IdResponse, status_code=201)
async def create(data: PostCreateDto, db: Session = Depends(get_db)):
    controller = PostController(db)
    return controller.create(data)


@router.get(
    "/{post_id}",
    response_model=PostResponseDto,
    responses={404: {"model": ErrorResponse}},
)
async def find_by_id(post_id: int, db: Session = Depends(get_db)):
    controller = PostController(db)
    return controller.find_by_id(post_id)


@router.get("/username/{posts_username}", response_model=List[PostResponseDto])
async def find_all_by_username(posts_username: str, db: Session = Depends(get_db)):
    controller = PostController(db)
    return controller.find_all_by_username(posts_username)


@router.patch("/{post_id}")
async def update(post_id: int, data: PostUpdateDto, db: Session = Depends(get_db)):
    controller = PostController(db)
    return controller.update(post_id, data)


@router.patch(
    "/archive/{post_id}",
    status_code=204,
    responses={404: {"model": ErrorResponse}, 409: {"model": ErrorResponse}},
)
async def archive(post_id: int, db: Session = Depends(get_db)):
    controller = PostController(db)
    return controller.archive(post_id)


@router.patch(
    "/unarchive/{post_id}",
    status_code=204,
    responses={404: {"model": ErrorResponse}, 409: {"model": ErrorResponse}},
)
async def unarchive(post_id: int, db: Session = Depends(get_db)):
    controller = PostController(db)
    return controller.unarchive(post_id)


@router.delete("/{post_id}", status_code=204, responses={404: {"model": ErrorResponse}})
async def delete(post_id: int, db: Session = Depends(get_db)):
    controller = PostController(db)
    return controller.delete(post_id)
