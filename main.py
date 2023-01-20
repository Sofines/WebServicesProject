import database
from fastapi import FastAPI, HTTPException, Body, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from auth import authenticate_user, Token
from datetime import datetime
from bson.objectid import ObjectId as ObjectId
from model import TaskCreate, TaskUpdate, UserCreate, UserUpdate, User, UserId, UserData
from typing import List
from email_validator import validate_email, EmailNotValidError
from database import tasks_collection, users_collection
from database import db
from database import (
    create_task,
    get_user_by_username,
    create_user,
    update_user,
    remove_user,
)

# an HTTP-specific exception class  to generate exception information

app = FastAPI()

origins = [
    "http://localhost:3000",
]

# what is a middleware? 
# software that acts as a bridge between an operating system or database and applications, especially on a network.

@app.get("/")
async def read_root():
    return {"Hello": "Tasnim"}

@app.post("/tasks")
async def create_task(task: TaskCreate= Body(...)):
    task_dict = task.dict()
    task_id = tasks_collection.insert_one(task_dict).inserted_id
    task_dict["_id"] = task_id
    return task_dict

@app.get("/tasks/{task_id}")
async def read_task(task_id:str):
    task = tasks_collection.find_one({"_id": task_id})
    return task

@app.put("/tasks/{task_id}")
async def update_task(task_id:str, task: TaskUpdate):
    result = tasks_collection.update_one({"_id": task_id}, {"$set": task.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task updated"}

@app.delete("/tasks/{task_id}")
async def delete_task(task_id:str):
    result = tasks_collection.delete_one({"_id": task_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted"}
#----------------------------------------------------------------------------
#post_method_user
@app.post("/users/", response_model=UserCreate)
async def create_user(user: UserCreate):
    user.created_at = datetime.now()
    user.updated_at = datetime.now()
    try:
        v = validate_email(user.email)  # validate and get info
        email = v["email"]  # replace with normalized form
    except EmailNotValidError as e:
        # email is not valid, exception message is human-readable
        raise ValueError(str(e))
    
    user_id = await create_user(user)
    if not user_id:
        raise HTTPException(status_code=400, detail="Could not create user.")
    return {"user_id": user_id}

#get_method_user
@app.get("/users/{username}/", response_model=User)
async def get_user_by_username(username: str):
    user = await users_collection.find_one({"username":username})
    return user

#put_method_user
@app.put("/users/{user_id}/", response_model=User)
async def update_user(user_id: str, user: UserUpdate):
    user_doc = user.dict(exclude_unset=True)
    result = await users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": user_doc})
    return user_doc

#delete_method_user
@app.delete("/users/{user_id}/", response_model=User)
async def remove_user(user_id: str):
    result = await users_collection.delete_one({"_id": ObjectId(user_id)})
    return {"message": "User removed"}

#------------------------------------------------------------------------------------------------
@app.post("/login", response_model=None)
async def login(user: User):
    # your code here
    return {"access_token": Token}
