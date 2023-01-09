from fastapi import FastAPI, Response, status, HTTPException, APIRouter
from .. import schemas, utils, db

router = APIRouter(prefix="/users", tags=['Users'])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user : schemas.UserCreate):
    pwd_hash = utils.hash(user.password)
    user.password = pwd_hash
    
    try:
        db.cur.execute("Insert into users(email, password) Values ( %s, %s) Returning *",(user.email,user.password))
        new_user = db.cur.fetchone()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'User with email {user.email} already exists. {e}') 
    db.conn.commit()
    return new_user

@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id : int):
    db.cur.execute("SELECT * FROM users Where id = %s", (str(id),))
    user = db.cur.fetchone()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id {str(id)} not found.')
    return user