from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.configs.env import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER


DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(
    DB_URL,
    pool_pre_ping=True,  # Verifica se a conexão está ativa antes de usar
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    Base.metadata.create_all(bind=engine)
