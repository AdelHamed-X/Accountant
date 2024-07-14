from fastapi import FastAPI, Depends
import psycopg
from psycopg.rows import dict_row
from . import models
from .database import engine, get_db
from app.routers import posts, users, auth


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

try:
    conn = psycopg.connect("host=localhost dbname=fastapi user=postgres password=admin123")
    cursor = conn.cursor(row_factory=dict_row)
    print('Database connection established successfully!')
except Exception as error:
    print('Connection to database failed!')
    print('Error: ', error)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)


@app.get('/')
async def root():
    return {"message": "Hello World"}
