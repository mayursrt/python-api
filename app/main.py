from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time


while True:
    try:
        conn = psycopg2.connect("host=localhost dbname=python-API user=postgres password=admin", cursor_factory=RealDictCursor)
        cur = conn.cursor()
        break
    except Exception as error:
        print("Connection Failed")

    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)


class Post(BaseModel):
    title : str
    content : str
    published : bool = True
    rating : Optional[int] = None

app = FastAPI()



@app.get("/posts")
def get_posts():
    cur.execute("SELECT * FROM posts LIMIT 100")
    posts = cur.fetchall()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post : Post):
    cur.execute("Insert into posts(title, content, published) Values (%s, %s, %s) Returning *",(post.title,post.content, post.published))
    new_post = cur.fetchone()
    conn.commit()
    return {"data":new_post}

@app.get("/posts/{id}")
def get_post(id : int):
    cur.execute("SELECT * FROM posts Where id = %s", str(id))
    posts = cur.fetchone()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id {str(id)} not found.')
    return {"data": posts}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int):
    cur.execute("DELETE from posts where id = %s Returning *", (str(id),))
    del_post = cur.fetchone()
    if not del_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id {str(id)} not found.')
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id : int, post : Post):
    cur.execute("Update posts Set title = %s, content = %s, published = %s Where id = %s Returning *", (post.title, post.content, post.published,str(id)))
    
    updated_post = cur.fetchone()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id {str(id)} not found.')
    conn.commit()
    return {"data" : updated_post}
    
    