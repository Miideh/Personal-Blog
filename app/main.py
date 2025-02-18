from fastapi import FastAPI, HTTPException,status, Request, StaticFiles

from fastapi.templating import Jinja2Templates 
from app.routes.routes import router
from app.models.model import Post, Home
app = FastAPI()

templates = Jinja2Templates(directory="app/templates") 
app.include_router(router) 



app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Personal Blog"}

@app.get("/home")
async def home(request: Request):
    posts = await Post.find().to_list(100)
    return templates.TemplateResponse("home.html", {"request": request, "posts": posts})

@app.get("/post/{date}")
async def post_detail(date: str, request: Request):
    post = await Post.find_one({"date": date})
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return templates.TemplateResponse("post_detail.html", {"request": request, "post": post})

@app.get("/dashboard")
async def dashboard(request: Request):
    posts = await Post.find().to_list(100)
    return templates.TemplateResponse("dashboard.html", {"request": request, "posts": posts})
