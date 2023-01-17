from fastapi import FastAPI, Response, status, HTTPException,Depends
from .routers import posts, users, auth


app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
