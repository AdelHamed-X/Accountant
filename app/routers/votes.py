from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schema, database, oauth2, models

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote_data: schema.Vote, db: Session = Depends(database.get_db),
         user: schema.TokenData = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote_data.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {post.id} doesn't exist")

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote_data.post_id, models.Vote.user_id == user.id)
    vote_found = vote_query.first()

    if vote_data.dir == 1:
        if vote_found:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You've already voted before!")
        new_vote = models.Vote(user_id=user.id, post_id=vote_data.post_id)
        db.add(new_vote)
        db.commit()
        return {"Message": "Successfully voted!"}
    else:
        if not vote_found:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You have not voted for this post yet!")
        db.delete(vote_found)
        db.commit()

        return {"Message": "Successfully unvoted!"}
