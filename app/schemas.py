from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint


class UserResponse(BaseModel):
    email : EmailStr
    id : int
    username : str
    class Config:
        orm_mode = True
    

class PostBase(BaseModel):
    title : str
    content : str
    published : bool = False
    class Config:
        orm_mode = True
    

class PostCreate(PostBase):
    pass
    
class PostUpdate(PostBase):
    pass


class PostResponse(PostBase):
    id : int
    owner : UserResponse
    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post : PostBase
    votes : int
    class Config:
        orm_mode = True


class AllPostsResponse(PostBase):
    id : int
    class Config:
        orm_mode = True
    

class UserCreate(BaseModel):
    email : EmailStr
    password : str
    username : str


class UserLogin(BaseModel):
    email : EmailStr
    password : str

class UserInfo(UserResponse):
    created_at : datetime


class Token(BaseModel):
    access_token : str
    token_type : str


class TokenData(BaseModel):
    id : Optional[str]


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)