from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional



class PostBase(BaseModel):
    title : str
    content : str
    published : bool = True
    class Config:
        orm_mode = True
    
    


class PostCreate(PostBase):
    pass
    
class PostUpdate(PostBase):
    pass

class PostResponse(PostBase):
    id : int
    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    email : EmailStr
    id : int
    created_at : datetime
    

class AllPostsResponse(PostBase):
    id : int
    class Config:
        orm_mode = True
    

class UserCreate(BaseModel):
    email : EmailStr
    password : str


class UserLogin(BaseModel):
    email : EmailStr
    password : str

class Token(BaseModel):
    access_token : str
    token_type : str


class TokenData(BaseModel):
    id : Optional[str]