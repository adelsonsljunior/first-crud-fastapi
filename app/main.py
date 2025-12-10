from fastapi import FastAPI
import uvicorn

from database import create_tables
from routes.post_router import router as post

create_tables()

app = FastAPI()
app.include_router(post)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
