from pydantic import BaseModel
from datetime import datetime


class BasePost(BaseModel):
    title: str
    content: str
    published: bool

    class Config:
        from_attributes = True


class CreatePost(BasePost):
    pass


class PostRespone(BasePost):
    id: int
