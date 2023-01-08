from fastapi import FastAPI, Response, status, HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import OperationalError, errorcodes, errors
import time
from . import schemas
from typing import List
from passlib.context import CryptContext


app = FastAPI()
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


while True:
    try:
        conn = psycopg2.connect("host=localhost dbname=python-api user=postgres password=admin", cursor_factory=RealDictCursor)
        cur = conn.cursor()
        break
    except Exception as error:
        print("Connection Failed")

    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)

@app.get("/posts", response_model=List[schemas.PostResponse])
def get_posts():
    cur.execute("SELECT * FROM posts LIMIT 100")
    posts = cur.fetchall()
    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post : schemas.PostCreate):
    cur.execute("Insert into posts(title, content, published) Values (%s, %s, %s) Returning *",(post.title,post.content, post.published))
    new_post = cur.fetchone()
    conn.commit()
    return new_post

@app.get("/posts/{id}", response_model=schemas.PostResponse)
def get_post(id : int):
    cur.execute("SELECT * FROM posts Where id = %s", (str(id),))
    posts = cur.fetchone()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id {str(id)} not found.')
    return posts

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int):
    cur.execute("DELETE from posts where id = %s Returning *", (str(id),))
    del_post = cur.fetchone()
    if not del_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id {str(id)} not found.')
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", response_model=schemas.PostResponse)
def update_post(id : int, post : schemas.PostUpdate):
    cur.execute("Update posts Set title = %s, content = %s, published = %s, updated_at = %s Where id = %s Returning *", (post.title, post.content, post.published, "now()",str(id)))
    
    updated_post = cur.fetchone()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id {str(id)} not found.')
    conn.commit()
    return updated_post
    

@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user : schemas.UserCreate):
    pwd_hash = pwd_context.hash(user.password)
    user.password = pwd_hash
    
    try:
        cur.execute("Insert into users(email, password) Values ( %s, %s) Returning *",(user.email,user.password))
        new_user = cur.fetchone()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'User with email {user.email} already exists. {e}') 
    conn.commit()
    return new_user
