from pydantic import BaseModel
from typing import Optional


class BasePost(BaseModel):
    title: str
    content: str

    class Config:
        from_attributes = True


class PostCreate(BasePost):
    pass


class PostRespone(BasePost):
    pass
