from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import status, Response
from fastapi.responses import JSONResponse

from models.post import Post
from schemas.post_schema import PostCreateDto
from schemas.responses import ErrorResponse, IdResponse


class PostController:
    def __init__(self, db: Session):
        self.db = db

    def find_all(self):
        return self.db.query(Post).all()

    def find_all_by_username(self, posts_username: str):
        posts_username = "%" + posts_username + "%"
        return self.db.query(Post).filter(Post.username.like(posts_username)).all()

    def create(self, data: PostCreateDto) -> IdResponse:
        post = Post(**data.model_dump())
        self.db.add(post)
        self.db.commit()
        self.db.refresh(post)
        return IdResponse(id=post.id)

    def find_by_id(self, post_id: int):
        post = self.db.query(Post).filter(Post.id == post_id).first()
        if not post:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=ErrorResponse(message="Post não encontrado").model_dump(),
            )
        return post

    def archive(self, post_id):
        post = self.db.query(Post).filter(Post.id == post_id).first()
        if not post:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=ErrorResponse(message="Post não encontrado").model_dump(),
            )

        if post.archived:
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content=ErrorResponse(message="Post já está arquivado").model_dump(),
            )

        post.archived = True
        post.updated_at = func.now()
        self.db.commit()

        return Response(status_code=status.HTTP_204_NO_CONTENT)


    def unarchive(self, post_id):
        post = self.db.query(Post).filter(Post.id == post_id).first()
        if not post:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=ErrorResponse(message="Post não encontrado").model_dump(),
            )

        if not post.archived:
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content=ErrorResponse(message="Post já está desarquivado").model_dump(),
            )

        post.archived = False
        post.updated_at = func.now()
        self.db.commit()

        return Response(status_code=status.HTTP_204_NO_CONTENT)