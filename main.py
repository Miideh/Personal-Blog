from fastapi import FastAPI
from routes import router
from models import Base
from starlette.templating import Jinja2Templates
import os




app = FastAPI()
app.include_router(router)

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "Templates"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
    
print(os.path.join(BASE_DIR, "templates"))
