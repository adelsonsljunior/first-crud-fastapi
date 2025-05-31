from sqlalchemy.orm import Session
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
        db_post = Post(**data.model_dump())
        self.db.add(db_post)
        self.db.commit()
        self.db.refresh(db_post)
        return IdResponse(id=db_post.id)

    def find_by_id(self, post_id: int):
        post = self.db.query(Post).filter(Post.id == post_id).first()
        if not post:
            return JSONResponse(
                status_code=404,
                content=ErrorResponse(message="Post não encontrado").model_dump(),
            )
        return post
