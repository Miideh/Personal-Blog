from fastapi import APIRouter, HTTPException,status, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter
from app.models.model import Post, Home


router = APIRouter()
post_list = []
templates = Jinja2Templates(directory="templates/")

@router.get("/")
async def home(request: Request):
    Post = await Post.find().to_list(100)
    for post in Post:
        post["_id"] = str(post["_id"])
    return templates.TemplateResponse("home.html", {"request": request, "post": Post})

@router.get("/post/{date}")
async def post_detail(date: str, request: Request):
    post = await post.find_one({"_id": date(date)})
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    post["_id"] = str(post["_id"])
    return templates.TemplateResponse("Post page.html", {"request": request, "post": post})



@router.post("/post/create")
async def create_post(title: str = Form(...), content: str = Form(...)):
    new_post = {"title": title, "content": content}
    result = await Post.insert_one(new_post)
    return {"message": "Post created successfully", "id": str(result.inserted_id)}

@router.post("/post/update/{date}")
async def update_post(date: str, title: str = Form(...), content: str = Form(...)):
    update_result = await Post.update_one(
        {"_id": date(date)},
        {"$set": {"title": title, "content": content}}
    )
    if update_result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Post not found or no update made")
    return {"message": "Post updated successfully"}



@router.delete("/post/delete/{date}")
async def delete_post(date: str):
    delete_result = await Post.delete_one({"_id": date(date)})
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"message": "Post deleted successfully"}

@router.get("/dashboard")
async def dashboard(request: Request):
    posts = await Post.find().to_list(100)
    for post in posts:
        post["_id"] = str(post["_id"])
    return templates.TemplateResponse("dashboard.html", {"request": request, "posts": post})


    
    

    
   
    
    
    
@router.delete("/{date}")
async def delete_post(date: int) -> dict:
    for post in post:
        if post.date == date:
            post.remove(post)
            return {
                "message": "Post deleted successfully"
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID does not exist"
    )