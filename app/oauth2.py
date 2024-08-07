import uuid
from datetime import datetime, timedelta
from jose import JWTError, jwt
from . import schema, database, models
from .config import setting
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = setting.secret_key
ALGORITHM = setting.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = setting.access_token_expire_minutes


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})

    jwt_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return jwt_token


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)

        id: uuid.UUID = payload.get("id")

        if not id:
            raise credentials_exception
        token_data = schema.TokenData(id=id)
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Couldn't validate credentials!",
                                          headers={"WWW-Authenticate": "Bearer"})
    id = verify_access_token(token, credentials_exception).id

    user = db.query(models.User).filter(models.User.id == id).first()
    return user
