from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from setting import settings

pwd_context = CryptContext(schemes=["argon2"], deprecated='auto')


def hash_password(password: str) -> str:
    return str(pwd_context.hash(password))


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


def create_access_token(data: dict) -> str:
    real_data = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.TOKEN_EXPIRATION_TIME)
    real_data.update({"exp": expire})
    return jwt.encode(real_data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
