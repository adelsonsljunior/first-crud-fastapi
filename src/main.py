import os
from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn

from database import create_tables
from routes.post_router import router as post

create_tables()

app = FastAPI()
app.include_router(post)

load_dotenv()
PORT = int(os.getenv("PORT", 8080))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=PORT)
