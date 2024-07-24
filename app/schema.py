import uuid

from pydantic import BaseModel, EmailStr, UUID4
from typing import Optional, Literal
from datetime import datetime


class BasePost(BaseModel):
    title: str
    content: str

    class Config:
        from_attributes = True


class PostCreate(BasePost):
    pass


class PostRespone(BasePost):
    # owner_id: uuid.UUID
    published: Optional[bool]
    id: uuid.UUID
    owner: "UserOut"


class PostVote(PostRespone):
    votes: int


class BaseUser(BaseModel):
    email: EmailStr
    password: str

    class Config:
        from_attributes = True


class UserOut(BaseModel):
    email: EmailStr
    id: UUID4
    created_at: datetime


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[uuid.UUID]


class Vote(BaseModel):
    post_id: UUID4
    dir: Literal[0, 1]
