from fastapi import FastAPI, Response, status, HTTPException,Depends
from .routers import posts, users, auth, votes
from sqlalchemy.orm import Session
from .db import get_db, engine
from . import models
app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)
