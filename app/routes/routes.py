from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.database.connection import SessionLocal
from app.models.model import Post, PostCreate, PostResponse
from datetime import datetime

router = APIRouter()  

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/posts/", response_model=PostResponse)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    date_published = datetime.now()
    excerpt = post.content[:100] if post.content else ""
    db_post = Post(
        title=post.title,
        author=post.author,
        content=post.content,
        date_published=date_published,
        excerpt=excerpt
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post