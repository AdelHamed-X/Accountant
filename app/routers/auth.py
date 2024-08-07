from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, schema, models, utils, oauth2

router = APIRouter(
    tags=['Authentication']
)


@router.post('/auth', response_model=schema.Token)
def login(user_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_data.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Invalid Credentials')

    if not utils.verify(user_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Invalid Credentials')

    access_token = oauth2.create_access_token(data={"id": f"{user.id}"})
    return {"access_token": access_token, "token_type": "bearer"}
