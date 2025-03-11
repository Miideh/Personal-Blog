from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
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