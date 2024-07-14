from .. import utils, models, schema
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends, APIRouter
import uuid

router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schema.UserOut)
def create_user(user: schema.BaseUser, db: Session = Depends(get_db)):
    hashed_pass = utils.hashed(user.password)
    user.password = hashed_pass

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get('/{id}', response_model=schema.UserOut)
def get_user(id: uuid.UUID, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with id: {id} was not found!')

    return user
