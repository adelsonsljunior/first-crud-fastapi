from models.post import Post
from schemas.post_schema import PostResponseDto


def post_entity_to_dto(entity: Post) -> PostResponseDto:
    return PostResponseDto(
        id=entity.id,
        username=entity.username,
        body=entity.body,
        archived=entity.archived,
        created_at=entity.created_at,
        updated_at=entity.updated_at,
    )


