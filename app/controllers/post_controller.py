from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import status, Response
from fastapi.responses import JSONResponse

from app.models.post import Post
from app.schemas.post_schema import PostCreateDto, PostUpdateDto, PostResponseDto
from app.schemas.responses import ErrorResponse, IdResponse, PaginationResponse
from app.mappers.post_mapper import post_entity_to_dto


class PostController:
    def __init__(self, db: Session):
        self.db = db

    def find_all(
        self,
        page: int,
        limit: int,
    ) -> PaginationResponse[PostResponseDto]:
        # Calcula o offset
        offset = (page - 1) * limit

        posts = self.db.query(Post).order_by(Post.id).offset(offset).limit(limit).all()
        total = self.db.query(Post).count()

        # Calcula o total de páginas (arredondando para cima)
        total_pages = max((total + limit - 1) // limit, 1)

        # Garante que a página atual está dentro dos limites
        current_page = min(max(page, 1), total_pages)

        # Convertendo a moda Python tudo em uma linha
        posts_dtos = [post_entity_to_dto(post) for post in posts]

        return PaginationResponse[PostResponseDto](
            data=posts_dtos,
            items_per_page=limit,
            total_items=total,
            current_page=current_page,
            total_pages=total_pages,
        )

    def find_all_by_username(
        self, posts_username: str, page: int, limit: int
    ) -> PaginationResponse[PostResponseDto]:
        offset = (page - 1) * limit

        posts_username = "%" + posts_username + "%"
        posts = (
            self.db.query(Post)
            .filter(Post.username.like(posts_username))
            .offset(offset)
            .limit(limit)
            .all()
        )
        total = self.db.query(Post).filter(Post.username.like(posts_username)).count()

        total_pages = max((total + limit - 1) // limit, 1)

        current_page = min(max(page, 1), total_pages)

        posts_dtos = [post_entity_to_dto(post) for post in posts]

        return PaginationResponse[PostResponseDto](
            data=posts_dtos,
            items_per_page=limit,
            total_items=total,
            current_page=current_page,
            total_pages=total_pages,
        )

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

    def update(self, post_id: int, data: PostUpdateDto):
        post = self.db.query(Post).filter(Post.id == post_id).first()
        if not post:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=ErrorResponse(message="Post não encontrado").model_dump(),
            )

        if data.body:
            post.body = data.body

        post.updated_at = func.now()
        self.db.commit()

        return Response(status_code=status.HTTP_204_NO_CONTENT)

    def archive(self, post_id: int):
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

    def unarchive(self, post_id: int):
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

    def delete(self, post_id: int):
        post = self.db.query(Post).filter(Post.id == post_id).first()
        if not post:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=ErrorResponse(message="Post não encontrado").model_dump(),
            )

        self.db.delete(post)
        self.db.commit()

        return Response(status_code=status.HTTP_204_NO_CONTENT)
