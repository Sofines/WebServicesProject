from datetime import datetime
from pydantic import BaseModel, EmailStr
from bson.objectid import ObjectId as ObjectId


class TaskCreate(BaseModel):
    title: str
    description: str
    deadline: datetime
    is_completed: bool

class TaskUpdate(BaseModel):
    status: str

class UserCreate(BaseModel):
    email: str
    password: str
    is_active: bool
    is_superuser: bool

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