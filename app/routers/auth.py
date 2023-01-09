from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from .. import schemas, db, utils, oauth2

router = APIRouter(tags=['Auth'])

@router.post("/login")
def login(user_creds : OAuth2PasswordRequestForm = Depends()):
    db.cur.execute("Select * from users where email = %s",(str(user_creds.username),))
    user = db.cur.fetchone()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Invalid Credentials')
    
    if not utils.verify(user_creds.password, user['password']):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Invalid Credentials')
    
    token = oauth2.create_access_token(data={"user_id":user['id']})
    
    return {"token": token, "token_type": "bearer"}