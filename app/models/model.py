from sqlalchemy import Column, Integer, String, DateTime
from app.database.connection import Base
from pydantic import BaseModel
from datetime import datetime

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    content = Column(String)
    date_published = Column(DateTime)
    excerpt = Column(String)

class PostCreate(BaseModel):
    title: str
    author: str
    content: str
    date_published: datetime = None
    excerpt: str = None

class PostResponse(BaseModel):
    id: int
    title: str
    author: str
    content: str
    date_published: datetime
    excerpt: str

    class Config:
        from_attributes = True  