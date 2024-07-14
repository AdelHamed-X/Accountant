from pydantic import BaseModel, EmailStr, UUID4
from typing import Optional
from datetime import datetime


class BasePost(BaseModel):
    title: str
    content: str

    class Config:
        from_attributes = True


class PostCreate(BasePost):
    pass


class PostRespone(BasePost):
    published: Optional[bool]
    id: int


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
