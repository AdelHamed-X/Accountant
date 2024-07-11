from fastapi import FastAPI, HTTPException, status, Response, Depends
from random import randrange
from pydantic import BaseModel
import psycopg
from psycopg.rows import dict_row
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

try:
    conn = psycopg.connect("host=localhost dbname=fastapi user=postgres password=admin123")
    cursor = conn.cursor(row_factory=dict_row)
    print('Database connection established successfully!')
except Exception as error:
    print('Connection to database failed!')
    print('Error: ', error)

my_posts = [
    {'id': 1, 'title': 'Python', 'content': 'Let\'s learn Python'},
    {'id': 2, 'title': 'SQL', 'content': 'Let\'s learn SQL'}
]


class Post(BaseModel):
    title: str
    content: str


def get_p(id: int):
    for p in my_posts:
        if p['id'] == id:
            return p


def get_index_post(id: int):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i
    return None


@app.get('/')
async def root():
    return {"message": "Hello World"}


@app.get('/sqlalchemy')
def test_posts(db: Session = Depends(get_db)):
    return {"detail": "Success!"}


@app.get("/posts")
def get_all_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}


@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute(f"""SELECT * FROM posts WHERE id = {id}""")
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={"message": f"post with id: {id} was not found!"})
    return {"data": post}


@app.post('/createpost', status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict()

    id = randrange(2, 1222222)
    title = post_dict['title']
    content = post_dict['content']

    cursor.execute(f"""INSERT INTO posts (id, title, content) VALUES ({id}, '{title}', '{content}')""")
    conn.commit()

    return get_post(id)


@app.delete('/deletepost/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("SELECT 1 FROM posts WHERE id = %s", (id,))

    if cursor.fetchone() is not None:
        cursor.execute("DELETE FROM posts WHERE id = %s", (id,))
        conn.commit()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={"message": f"post with id: {id} was not found!"})
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/updatepost/{id}')
def update_post(id: int, post: Post):
    cursor.execute("SELECT 1 FROM posts WHERE id = %s", (id,))

    if cursor.fetchone() is not None:
        title = post.dict()['title']
        content = post.dict()['content']
        cursor.execute("UPDATE posts SET title = %s, content = %s WHERE id = %s RETURNING *", (title, content, id))
        updated_post = cursor.fetchone()
        conn.commit()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={"message": f"post with id: {id} was not found!"})

    return {"data": updated_post}
