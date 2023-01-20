from datetime import datetime
from pydantic import BaseModel, EmailStr
from bson.objectid import ObjectId as ObjectId
from bson.errors import InvalidId
from typing import Any




class TaskCreate(BaseModel):
    title: str
    description: str
    deadline: datetime
    is_completed: bool

class TaskUpdate(BaseModel):
    status: str

class UserCreate(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    created_at: datetime = None
    updated_at: datetime = None
    class Config:
        allow_mutation = True

class UserUpdate(BaseModel):
    username: str = None
    email: str = None

class Task(BaseModel):
    title: str
    description: str
    done: bool
    created_at: datetime
    updated_at: datetime
    user_id: str

class User(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    created_at: datetime
    updated_at: datetime

def valid_oid(value: Any) -> ObjectId:
    try:
        return ObjectId(value)
    except InvalidId:
        raise


class UserId(BaseModel):
    id: ObjectId
    class Config:
        arbitrary_types_allowed = True


class UserData(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    created_at: datetime
    updated_at: datetime

