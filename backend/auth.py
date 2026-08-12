from datetime import datetime, timedelta
from jose import jwt 
from passlib.context import CryptContext
from setting import settings
from typing import Annotated
from pydantic import Field


pwd_context = CryptContext(schemes=["argon2"],deprecated='auto')

def hash_password(password:Annotated[str,Field(max_length=50)]):
    return str(pwd_context.hash(password))

def verify_password(password,hashed_password):
   return pwd_context.verify(password,hashed_password)

def create_access_token(data:dict):
    real_data = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=settings.TOKEN_EXPIRATION_TIME)

    real_data.update({"exp":expire})

    encoded_jwt = jwt.encode(real_data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return encoded_jwt