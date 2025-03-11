from fastapi import FastAPI
from routes import router
from models import Base
from connection import engine
from starlette.templating import Jinja2Templates
import os


Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
    
print(os.path.join(BASE_DIR, "templates"))
