from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
from typing import Optional
from bson import ObjectId, errors as bson_errors
from connection import posts_collection

router = APIRouter()
templates = Jinja2Templates(directory="Templates")

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    posts = list(posts_collection.find())
    return templates.TemplateResponse("home.html", {"request": request, "posts": posts})


@router.get("/post/{id}", response_class=HTMLResponse)
async def post_page(request: Request, id: str):
    try:
        post = posts_collection.find_one({"_id": ObjectId(id)})
        if post is None:
            raise HTTPException(status_code=404, detail="Post not found")
    except bson_errors.InvalidId:
        print(f"Invalid ID format: {id}")
        raise HTTPException(status_code=400, detail="Invalid ID format")
    return templates.TemplateResponse("post.html", {"request": request, "post": post})


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    posts = list(posts_collection.find())
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
):
    new_post = {
        "title": title,
        "excerpt": excerpt,
        "content": content,
        "author": author,
        "image_url": image_url,
        "date_published": datetime.now()
    }
    posts_collection.insert_one(new_post)
    posts = list(posts_collection.find())
    return templates.TemplateResponse("dashboard.html", {"request": request, "posts": posts})


@router.get("/dashboard/edit/{id}", response_class=HTMLResponse)
async def edit_post_form(request: Request, id: str):
    try:
        post = posts_collection.find_one({"_id": ObjectId(id)})
        if post is None:
            raise HTTPException(status_code=404, detail="Post not found")
    except bson_errors.InvalidId:
        raise HTTPException(status_code=400, detail="Invalid ID format")
    return templates.TemplateResponse("edit.html", {"request": request, "post": post})


@router.post("/dashboard/edit/{id}", response_class=HTMLResponse)
async def edit_post_submit(
    request: Request,
    id: str,
    title: str = Form(...),
    excerpt: str = Form(...),
    content: str = Form(...),
    author: str = Form(...),
    image_url: Optional[str] = Form(None),
):
    try:
        posts_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": {
                "title": title,
                "excerpt": excerpt,
                "content": content,
                "author": author,
                "image_url": image_url,
            }}
        )
    except bson_errors.InvalidId:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    posts = list(posts_collection.find())
    return templates.TemplateResponse("dashboard.html", {"request": request, "posts": posts})


@router.post("/dashboard/delete/{id}", response_class=HTMLResponse)
async def delete_post_submit(request: Request, id: str):
    try:
        posts_collection.delete_one({"_id": ObjectId(id)})
    except bson_errors.InvalidId:
        print(f"Invalid ID format: {id}")
        raise HTTPException(status_code=400, detail="Invalid ID format")

    posts = list(posts_collection.find())
    return templates.TemplateResponse("dashboard.html", {"request": request, "posts": posts})

