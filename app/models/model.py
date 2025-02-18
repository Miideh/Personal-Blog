from pydantic import BaseModel




class Post(BaseModel):
    authorname: str
    blogpost: str
    date: int
    

class Home(BaseModel):
    title: str
    excerpt: str
    image:str
    Post: Post
    
    
    