from fastapi import FastAPI, Response, status, HTTPException, APIRouter, Depends
from .. import schemas, db, oauth2, models
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func

router = APIRouter(prefix="/posts", tags=['Posts'])

@router.get("/all", response_model=List[schemas.AllPostsResponse])
def get_all_posts(db: Session = Depends(db.get_db), limit : int = 10, skip : int = 0, search : Optional[str] = ""):
    # db.cur.execute("SELECT * FROM posts Where published = True order by created_at DESC")
    # db.cur.execute("SELECT p.id, p.title, p.content, p.published, u.username FROM posts p join users u on u.id = p.created_by where p.published = true AND LOWER(p.title) LIKE %s ORDER BY p.created_at DESC LIMIT %s OFFSET %s",("%"+search.lower()+"%",str(limit), str(skip)))
    # posts = db.cur.fetchall()
    posts = db.query(models.Post).filter(func.lower(models.Post.title).contains(str(search.lower()))&(models.Post.published==True)).limit(limit).offset(skip).all()
    return posts


@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(db.get_db), current_user: int = Depends(oauth2.get_current_user)):
    # db.cur.execute("SELECT * FROM posts Where created_by = %s", (str(current_user['id']),))
    # posts = db.cur.fetchall()
    posts = db.query(models.Post).filter(models.Post.created_by == current_user.id).all()
    return posts


@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id : int,db: Session = Depends(db.get_db), current_user: int = Depends(oauth2.get_current_user)):
    # db.cur.execute("SELECT * FROM posts Where id = %s and created_by = %s", (str(id),current_user['id']))
    # post = db.cur.fetchone()
    post = db.query(models.Post).filter((models.Post.id == id)&(models.Post.created_by == current_user.id)).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id {str(id)} not found for current user.')
    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post : schemas.PostCreate, db: Session = Depends(db.get_db), current_user: int = Depends(oauth2.get_current_user)):
    # db.cur.execute("Insert into posts(title, content, published, created_by) Values (%s, %s, %s, %s) Returning *",(post.title,post.content, post.published, current_user['id']))
    # new_post = db.cur.fetchone()
    # db.conn.commit()
    new_post = models.Post(**post.dict(), created_by = current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int, db: Session = Depends(db.get_db), current_user: int = Depends(oauth2.get_current_user)):
    # db.cur.execute("DELETE from posts where id = %s and created_by = %s Returning *", (str(id),current_user['id']))
    # del_post = db.cur.fetchone()
    del_post = db.query(models.Post).filter((models.Post.id == id)&(models.Post.created_by == current_user.id))    
    if not del_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id {str(id)} not found for current user.')
    del_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id : int, post : schemas.PostUpdate, db: Session = Depends(db.get_db), current_user: int = Depends(oauth2.get_current_user)):
    # db.cur.execute("Update posts Set title = %s, content = %s, published = %s, updated_at = %s Where id = %s and created_by = %s Returning *", (post.title, post.content, post.published, "now()",str(id), current_user['id']))
    # updated_post = db.cur.fetchone()
    
    query = db.query(models.Post).filter((models.Post.id == id)&(models.Post.created_by == current_user.id))
    if not query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id {str(id)} not found.')
    query.update(post.dict(), synchronize_session=False)
    db.commit()
    updated_post = query.first()
    return updated_post
