import uuid
from typing import List, Optional
from .. import models, schema, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException, status, Response, Depends, APIRouter

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)


@router.get("/", response_model=List[schema.PostVote])
def get_all_posts(db: Session = Depends(get_db), limit: int = 10,
                  skip: int = 0, search: Optional[str] = ""):

    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes"), models.User).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).join(
        models.User, models.Post.owner_id == models.User.id).group_by(
        models.Post.id, models.User.id).filter(
        models.Post.title.contains(search)).limit(
        limit).offset(skip).all()

    resp = []
    for result in results:
        obj_data = result[0].__dict__.copy()
        obj_data["votes"] = result[1]
        obj_data["owner"] = result[2]
        resp.append(obj_data)

    return resp


@router.get("/{id}")
def get_post(id: uuid.UUID, db: Session = Depends(get_db),
             user: schema.TokenData = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={"message": f"post with id: {id} was not found!"})
    return post


@router.post('/createpost', status_code=status.HTTP_201_CREATED, response_model=schema.PostRespone)
def create_post(post: schema.PostCreate, db: Session = Depends(get_db),
                user: schema.TokenData = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id=user.id, **post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.delete('/deletepost/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: uuid.UUID, db: Session = Depends(get_db),
                user: schema.TokenData = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if user.id != post.owner_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not Allowed Here!")

    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={"message": f"post with id: {id} was not found!"})
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/updatepost/{id}', response_model=schema.PostRespone)
def update_post(id: uuid.UUID, post: schema.PostCreate, db: Session = Depends(get_db),
                user: schema.TokenData = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    existing_post = post_query.first()

    if existing_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={"message": f"post with id: {id} was not found!"})

    if user.id != existing_post.owner_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not Allowed Here!")

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post
