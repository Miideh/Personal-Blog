from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from passlib.hash import bcrypt
from datetime import datetime

Base = declarative_base()

class BlogPost(Base):
    __tablename__ = "blog_posts"  

    id = Column(Integer, primary_key=True, index=True) 
    title = Column(String, index=True)                  
    excerpt = Column(String)                            
    content = Column(String)                            
    author = Column(String)                             
    date_published = Column(DateTime, default=datetime.now) 
    image_url = Column(String, nullable=True)         
    
    
    
class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, unique=True, index=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    def verify_password(self, password: str) -> bool:
        return bcrypt.verify(password, self.hashed_password)  