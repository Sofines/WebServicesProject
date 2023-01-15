import jwt
import json
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from pydantic import BaseModel, ValidationError
from pymongo import MongoClient, ReturnDocument
from bson.objectid import ObjectId as ObjectId
from pymongo.errors import OperationFailure
from datetime import datetime, timedelta
from typing import Optional, Dict
import datetime
from model import User
from database import get_user_by_username, users_collection, connect_to_db, db

credentials_exception = HTTPException(status_code=400, detail="Incorrect username or password")
from config import SECRET_KEY, ALGORITHM
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Token:
    SECRET_KEY = "my_secret_key"
    ALGORITHM = "HS256"

    @staticmethod
    def create_access_token(data: Dict[str,str], expires_delta: timedelta = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, Token.SECRET_KEY, algorithm=Token.ALGORITHM)
        return encoded_jwt.decode()
    
    @staticmethod
    def decode_access_token(encoded_token: str):
        decoded_token = jwt.decode(encoded_token, Token.SECRET_KEY, algorithms=[Token.ALGORITHM])
        return decoded_token


class TokenData(BaseModel):
    username: str
    exp: int

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

#create_access_token:
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

#get_user:
def get_user(db, username: str):
    if not username:
        return None
    return db.users.find_one({"username": username})

#authenticate_user:
def authenticate_user(username: str, password: str):
    user = users_collection.find_one({"username": username})
    if not user:
        return False
    if not pwd_context.verify(password, user["password"]):
        return False
    return user

#get_password_hash:
def get_password_hash(password: str):
    return pwd_context.hash(password)

#verify_pass:
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

#get_current_user
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

#get_current_active_user:
async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

#get_user_by_username
async def get_user_by_username(username: str):
    db = connect_to_db()
    users_collection = db["users"]
    user = users_collection.find_one({"username": username})
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    return user

#check_token
def check_token(encoded_token: str):
    try:
        payload = jwt.decode(encoded_token, SECRET_KEY)
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=400, detail="Token is invalid")
    except (JWTError, ValidationError):
        raise HTTPException(status_code=400, detail="Token is invalid")
    user = get_user_by_username(username=username)
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    return user
