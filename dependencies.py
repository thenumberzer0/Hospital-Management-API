from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from sqlalchemy import select
from database import get_db
from models import Workers, Permissions
from setting import settings
from typing import Annotated

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/workers/login")


def get_currentUser(token: Annotated[str, Depends(oauth2_scheme)], db: Annotated[Session, Depends(get_db)]) -> Workers:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=403, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid token")

    user = db.execute(select(Workers).where(Workers.id == user_id)).scalars().first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user


def require_permissions(required_permissions: list[str]):
    def checker(
        db: Annotated[Session, Depends(get_db)],
        current_user: Annotated[Workers, Depends(get_currentUser)],
    ) -> Workers:
        granted = db.execute(
            select(Permissions.perm).where(Permissions.role == current_user.role)
        ).scalars().all()
        if not any(perm in granted for perm in required_permissions):
            raise HTTPException(status_code=401, detail="Unauthorized")
        return current_user

    return checker
