from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["blog_database"]  
posts_collection = db["posts"]  
users_collection = db["users"]
