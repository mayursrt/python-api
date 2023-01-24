from fastapi import FastAPI, Response, status, HTTPException, APIRouter, Depends
from .. import schemas, utils, db, models, oauth2
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users", tags=['Users'])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user : schemas.UserCreate, db: Session = Depends(db.get_db)):
    pwd_hash = utils.hash(user.password)
    user.password = pwd_hash
    
    try:
        # db.cur.execute("Insert into users(email, password) Values ( %s, %s) Returning *",(user.email,user.password))
        # new_user = db.cur.fetchone()
        new_user = models.User(**user.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'User with email {user.email} already exists. {e}') 
    
    return new_user


@router.get("/me", response_model=schemas.UserInfo)
def get_user(db: Session = Depends(db.get_db), current_user: int = Depends(oauth2.get_current_user)):
    # db.cur.execute("SELECT * FROM users Where id = %s", (str(id),))
    # user = db.cur.fetchone()
    user = db.query(models.User).filter(models.User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id {str(id)} not found.')
    return user


@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id : int, db: Session = Depends(db.get_db)):
    # db.cur.execute("SELECT * FROM users Where id = %s", (str(id),))
    # user = db.cur.fetchone()
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id {str(id)} not found.')
    return user
