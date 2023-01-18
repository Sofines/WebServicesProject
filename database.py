from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId
from typing import Dict, Any
from pydantic import BaseModel


client = MongoClient("mongodb://localhost:27017/")
db = client["task_management"]
tasks_collection = db["tasks"]
users_collection = db["users"]

class User(BaseModel):
    username: str
    email: str
    password: str
    full_name: str
    disabled: bool = False

def connect_to_db():
    return db
#---------------------------------------------------------------------------------------------------
async def create_user(user: Dict[str, Any]) -> None:
    # Insert the user into the users collection
    result = users_collection.insert_one(user)
    print(f"Inserted user with id: {result.inserted_id}")

async def get_user_by_username(username: str) -> Dict[str, Any]:
    # Find the user with the matching username
    user = users_collection.find_one({"username": username})
    return user

async def update_user(user_id: str, updated_user: dict):
    users_collection = db["users"]
    result = users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": updated_user})
    return result.modified_count

async def remove_user(user_id: str):
    users_collection = db["users"]
    result = users_collection.delete_one({"_id": ObjectId(user_id)})
    return result.deleted_count

#-----------------------------------------------------------------------------

async def create_task(task: dict):
    db = connect_to_db()
    tasks_collection = db.tasks
    tasks_collection.insert_one(task)

async def get_tasks(owner_id: str):
    db = connect_to_db()
    tasks_collection = db.tasks
    tasks = tasks_collection.find({"owner_id": owner_id})
    return tasks

async def update_task(task_id:str, task: dict):
    db = connect_to_db()
    tasks_collection = db.tasks
    tasks_collection.update_one({"_id": task_id}, {"$set": task})

async def delete_task(task_id: str):
    db = connect_to_db()
    tasks_collection = db.tasks
    tasks_collection.delete_one({"_id": task_id})

