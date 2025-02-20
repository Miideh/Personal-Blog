from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database.connection import engine, SessionLocal, Base
from app.routes.routes import router
from app.models.model import Post
from datetime import datetime  
import uvicorn

app = FastAPI()
app.include_router(router)
templates = Jinja2Templates(directory="templates")

Base.metadata.create_all(bind=engine)

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = None
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    db: Session = request.state.db
    posts = db.query(Post).all()
    return templates.TemplateResponse("homepage.html", {"request": request, "posts": posts})

@app.get("/post/{post_id}", response_class=HTMLResponse)
async def post(request: Request, post_id: int):
    db: Session = request.state.db
    post = db.query(Post).filter(Post.id == post_id).first()
    return templates.TemplateResponse("postpage.html", {"request": request, "post": post})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    db: Session = request.state.db
    posts = db.query(Post).all()
    return templates.TemplateResponse("dashboard.html", {"request": request, "posts": posts})

@app.get("/create", response_class=HTMLResponse)
async def create_get(request: Request):
    return templates.TemplateResponse("create.html", {"request": request})

@app.post("/create", response_class=HTMLResponse)
async def create_post(request: Request, title: str = Form(...), author: str = Form(...), content: str = Form(...)):
    db: Session = request.state.db
    date_published = datetime.now()
    excerpt = content[:100]
    new_post = Post(title=title, author=author, content=content, date_published=date_published, excerpt=excerpt)
    db.add(new_post)
    db.commit()
    return RedirectResponse(url="/dashboard", status_code=303)

@app.get("/edit/{post_id}", response_class=HTMLResponse)
async def edit_get(request: Request, post_id: int):
    db: Session = request.state.db
    post = db.query(Post).filter(Post.id == post_id).first()
    return templates.TemplateResponse("edit.html", {"request": request, "post": post})

@app.post("/edit/{post_id}", response_class=HTMLResponse)
async def edit_post(request: Request, post_id: int, title: str = Form(...), author: str = Form(...), content: str = Form(...)):
    db: Session = request.state.db
    post = db.query(Post).filter(Post.id == post_id).first()
    post.title = title
    post.author = author
    post.content = content
    db.commit()
    return RedirectResponse(url="/dashboard", status_code=303)

@app.get("/delete/{post_id}", response_class=HTMLResponse)
async def delete_post(request: Request, post_id: int):
    db: Session = request.state.db
    post = db.query(Post).filter(Post.id == post_id).first()
    db.delete(post)
    db.commit()
    return RedirectResponse(url="/dashboard", status_code=303)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)