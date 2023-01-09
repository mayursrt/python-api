from pydantic import BaseModel, EmailStr
from datetime import datetime

class PostBase(BaseModel):
    title : str
    content : str
    published : bool = True


class PostCreate(PostBase):
    pass
    
class PostUpdate(PostBase):
    pass

class PostResponse(PostBase):
    id : int


class UserCreate(BaseModel):
    email : EmailStr
    password : str

class UserResponse(BaseModel):
    email : EmailStr
    id : int
    created_at : datetime
    
class UserLogin(BaseModel):
    email : EmailStr
    password : str