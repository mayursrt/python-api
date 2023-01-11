from fastapi import FastAPI, Response, status, HTTPException, APIRouter, Depends
from .. import schemas, db, oauth2
from typing import List


router = APIRouter(prefix="/posts", tags=['Posts'])

@router.get("/published", response_model=List[schemas.PostResponse])
def get_posts():
    db.cur.execute("SELECT * FROM posts Where published = True order by created_at DESC")
    posts = db.cur.fetchall()
    return posts


@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(current_user: int = Depends(oauth2.get_current_user)):
    db.cur.execute("SELECT * FROM posts Where created_by = %s", (str(current_user['id']),))
    posts = db.cur.fetchall()
    return posts


@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id : int, current_user: int = Depends(oauth2.get_current_user)):
    db.cur.execute("SELECT * FROM posts Where id = %s and created_by = %s", (str(id),current_user['id']))
    posts = db.cur.fetchone()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id {str(id)} not found for current user.')
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post : schemas.PostCreate, current_user: int = Depends(oauth2.get_current_user)):
    db.cur.execute("Insert into posts(title, content, published, created_by) Values (%s, %s, %s, %s) Returning *",(post.title,post.content, post.published, current_user['id']))
    new_post = db.cur.fetchone()
    db.conn.commit()
    return new_post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int, current_user: int = Depends(oauth2.get_current_user)):
    db.cur.execute("DELETE from posts where id = %s and created_by = %s Returning *", (str(id),current_user['id']))
    del_post = db.cur.fetchone()
    if not del_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id {str(id)} not found for current user.')
    db.conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id : int, post : schemas.PostUpdate, current_user: int = Depends(oauth2.get_current_user)):
    db.cur.execute("Update posts Set title = %s, content = %s, published = %s, updated_at = %s Where id = %s and created_by = %s Returning *", (post.title, post.content, post.published, "now()",str(id), current_user['id']))
    
    updated_post = db.cur.fetchone()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id {str(id)} not found.')
    db.conn.commit()
    return updated_post
