from models.post import Post
from sqlalchemy.orm import Session

from schemas.post_schema import PostCreateDto


class PostController:
    def __init__(self, db: Session):
        self.db = db

    def find_all(self):
        return self.db.query(Post).all()

    def create(self, data: PostCreateDto):
        db_post = Post(**data.model_dump())
        self.db.add(db_post)
        self.db.commit()
        self.db.refresh(db_post)
        return db_post.id
