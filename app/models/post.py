from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from app.configs.database import Base


class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    body = Column(String, nullable=False)
    archived = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
