from pydantic import BaseSettings
from pymongo import MongoClient


SECRET_KEY = "my_secret_key"
ALGORITHM = "HS256"

class Config:
    client = MongoClient("mongodb://localhost:27017/")
    db = client["task_management"]
    tasks_collection = db["tasks"]
    users_collection = db["users"]

    CLIENT_ORIGIN= ["http://localhost:3000"]
    


    






    