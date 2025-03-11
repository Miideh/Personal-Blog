from fastapi import APIRouter, Request, Form, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from models import BlogPost
from connection import get_db
from datetime import datetime
from typing import Optional
from database import SessionLocal


router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    posts = db.query(BlogPost).all()
    return templates.TemplateResponse("home.html", {"request": request, "posts": posts})

@router.get("/post/{id}", response_class=HTMLResponse)
async def post_page(request: Request, id: int, db: Session = Depends(get_db)):
    post = db.query(BlogPost).filter(BlogPost.id == id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return templates.TemplateResponse("post.html", {"request": request, "post": post})

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, db: Session = Depends(get_db)):
    posts = db.query(BlogPost).all()
    return templates.TemplateResponse("dashboard.html", {"request": request, "posts": posts})

@router.get("/dashboard/create", response_class=HTMLResponse)
async def create_post_form(request: Request):
    return templates.TemplateResponse("create.html", {"request": request})

@router.post("/dashboard/create", response_class=HTMLResponse)
async def create_post_submit(
    request: Request,
    title: str = Form(...),
    excerpt: str = Form(...),
    content: str = Form(...),
    author: str = Form(...),
    image_url: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    new_post = BlogPost(
        title=title,
        excerpt=excerpt,
        content=content,
        author=author,
        image_url=image_url,
        date_published=datetime.now()
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    posts = db.query(BlogPost).all()
    return templates.TemplateResponse("dashboard.html", {"request": request, "posts": posts})

@router.get("/dashboard/edit/{id}", response_class=HTMLResponse)
async def edit_post_form(request: Request, id: int, db: Session = Depends(get_db)):
    post = db.query(BlogPost).filter(BlogPost.id == id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return templates.TemplateResponse("edit.html", {"request": request, "post": post})

@router.post("/dashboard/edit/{id}", response_class=HTMLResponse)
async def edit_post_submit(
    request: Request,
    id: int,
    title: str = Form(...),
    excerpt: str = Form(...),
    content: str = Form(...),
    author: str = Form(...),
    image_url: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    post = db.query(BlogPost).filter(BlogPost.id == id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    post.title = title
    post.excerpt = excerpt
    post.content = content
    post.author = author
    post.image_url = image_url
    db.commit()
    posts = db.query(BlogPost).all()
    return templates.TemplateResponse("dashboard.html", {"request": request, "posts": posts})

@router.post("/dashboard/delete/{id}", response_class=HTMLResponse)
async def delete_post_submit(request: Request, id: int, db: Session = Depends(get_db)):
    post = db.query(BlogPost).filter(BlogPost.id == id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()
    posts = db.query(BlogPost).all()
    return templates.TemplateResponse("dashboard.html", {"request": request, "posts": posts})