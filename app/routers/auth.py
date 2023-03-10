from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from .. import schemas, db, utils, oauth2, models
from sqlalchemy.orm import Session

router = APIRouter(tags=['Auth'])

@router.post("/login", response_model=schemas.Token)
def login(user_creds : OAuth2PasswordRequestForm = Depends(), db: Session = Depends(db.get_db)):
    # db.cur.execute("Select * from users where email = %s",(str(user_creds.username),))
    # user = db.cur.fetchone()
    user = db.query(models.User).filter((models.User.email == user_creds.username)|(models.User.username == user_creds.username)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Invalid Credentials')
    
    if not utils.verify(user_creds.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Invalid Credentials')
    
    token = oauth2.create_access_token(data={"user_id":user.id})

    return {"access_token" : token , "token_type" : "bearer"}