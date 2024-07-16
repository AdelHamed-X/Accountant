from fastapi import FastAPI, Depends
from . import models
from .database import engine, get_db
from app.routers import posts, users, auth


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)


@app.get('/')
async def root():
    return {"message": "Hello World"}
