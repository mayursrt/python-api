from fastapi import FastAPI, Response, status, HTTPException,Depends
from .routers import posts, users, auth
from sqlalchemy.orm import Session
from .db import get_db, engine
from . import models
app = FastAPI()

models.Base.metadata.create_all(bind=engine)

@app.get("/abc")
def test(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"Status":posts}

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
