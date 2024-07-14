import uuid

from .. import utils, models, schema
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends, APIRouter

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)


@router.get("/")
def get_all_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts


@router.get("/{id}")
def get_post(id: uuid.UUID, db: Session = Depends(get_db)):
    # cursor.execute(f"""SELECT * FROM posts WHERE id = {id}""")
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={"message": f"post with id: {id} was not found!"})
    return post


@router.post('/createpost', status_code=status.HTTP_201_CREATED)
def create_post(post: schema.PostCreate, db: Session = Depends(get_db)):
    # post_dict = post.dict()
    #
    # id = randrange(2, 1222222)
    # title = post_dict['title']
    # content = post_dict['content']
    #
    # cursor.execute(f"""INSERT INTO posts (id, title, content) VALUES ({id}, '{title}', '{content}')""")
    # conn.commit()

    new_post = models.Post(**post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.delete('/deletepost/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("SELECT 1 FROM posts WHERE id = %s", (id,))
    #
    # if cursor.fetchone() is not None:
    #     cursor.execute("DELETE FROM posts WHERE id = %s", (id,))
    #     conn.commit()
    # else:
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={"message": f"post with id: {id} was not found!"})
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# TODO - FIX UPDATE METHOD
@router.put('/updatepost/{id}', response_model=schema.PostRespone)
def update_post(id: uuid.UUID, post: schema.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("SELECT 1 FROM posts WHERE id = %s", (id,))
    #
    # if cursor.fetchone() is not None:
    #     title = post.dict()['title']
    #     content = post.dict()['content']
    #     cursor.execute("UPDATE posts SET title = %s, content = %s WHERE id = %s RETURNING *", (title, content, id))
    #     updated_post = cursor.fetchone()
    #     conn.commit()
    # else:
    post_query = db.query(models.Post).filter(models.Post.id == id)
    existing_post = post_query.first()
    print(post.dict())

    if existing_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={"message": f"post with id: {id} was not found!"})

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post