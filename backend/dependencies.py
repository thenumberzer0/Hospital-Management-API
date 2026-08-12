from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from sqlalchemy.orm import Session
from database import get_db
from models import Workers
from setting import settings
from typing import Annotated


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_currentUser(token:Annotated[str,Depends(oauth2_scheme)], db:Annotated[Session,Depends(get_db)],required_permissions:list[str]|None=None):
    
    try:
        payload = jwt.decode(token,settings.SECRET_KEY,algorithms=[settings.ALGORITHM])

        user_id = payload.get("user_id")
        
       



        if user_id is None:
            raise HTTPException(status_code=403,detail="Invalid token")
        if(required_permissions):
            permissions = payload.get("permissions")
            allow_access = [i for i in required_permissions if i in permissions]
            if allow_access is None:
                raise HTTPException(status_code=401,detail="Unauthorized")
        
    except:
         raise HTTPException(status_code=403,detail="Invalid token")


    

    user = db.query(Workers).where(Workers.id == user_id).first()

    if not user:
        raise HTTPException(status_code=401,detail="User not found")
    
    return user