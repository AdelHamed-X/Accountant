import uuid
from sqlalchemy import Column, ForeignKey, String, Boolean, DateTime, UUID
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime


class BaseModel(Base):
    __abstract__ = True
    id = Column(UUID(as_uuid=True), default=uuid.uuid4, nullable=False, unique=True, primary_key=True)
    created_at = Column(DateTime(timezone=True), default=datetime.now(), nullable=False)


class Post(BaseModel):
    __tablename__ = "posts"

    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="True")
    owner_id = Column(UUID, ForeignKey("users.id",
                      ondelete="CASCADE"), nullable=False)
    owner = relationship("User")


class User(BaseModel):
    __tablename__ = "users"

    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)


