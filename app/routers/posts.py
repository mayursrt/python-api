from fastapi import FastAPI, Response, status, HTTPException, APIRouter
from .. import schemas, db
from typing import List


router = APIRouter(prefix="/posts", tags=['Posts'])

@router.get("/", response_model=List[schemas.PostResponse])
def get_posts():
    db.cur.execute("SELECT * FROM posts LIMIT 100")
    posts = db.cur.fetchall()
    return posts


@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id : int):
    db.cur.execute("SELECT * FROM posts Where id = %s", (str(id),))
    posts = db.cur.fetchone()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id {str(id)} not found.')
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post : schemas.PostCreate):
    db.cur.execute("Insert into posts(title, content, published) Values (%s, %s, %s) Returning *",(post.title,post.content, post.published))
    new_post = db.cur.fetchone()
    db.conn.commit()
    return new_post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int):
    db.cur.execute("DELETE from posts where id = %s Returning *", (str(id),))
    del_post = db.cur.fetchone()
    if not del_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id {str(id)} not found.')
    db.conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id : int, post : schemas.PostUpdate):
    db.cur.execute("Update posts Set title = %s, content = %s, published = %s, updated_at = %s Where id = %s Returning *", (post.title, post.content, post.published, "now()",str(id)))
    
    updated_post = db.cur.fetchone()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id {str(id)} not found.')
    db.conn.commit()
    return updated_post
