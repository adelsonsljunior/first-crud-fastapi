import os

from dotenv import load_dotenv

from database import create_tables

from fastapi import FastAPI
from routes.post_router import router as post

app = FastAPI()
app.include_router(post)

create_tables()


load_dotenv()
PORT = int(os.getenv("PORT", 8080))
