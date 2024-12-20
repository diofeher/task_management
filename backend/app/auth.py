import jwt
from typing import Dict, Annotated, cast, Any
from passlib.hash import pbkdf2_sha256
from jwt.exceptions import InvalidTokenError

from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.sql import ColumnElement
from sqlalchemy.orm import Session
from sqlalchemy import select

from .db import get_session
from .users.models import User, TokenData

# TODO: Pass as configuration, hardcoded for now
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")


def create_access_token(
    data: Dict[str, str | datetime], expires_delta: timedelta | None = None
) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = str(jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM))
    return encoded_jwt


def hash_password(password: str) -> str:
    return str(pbkdf2_sha256.hash(password))


async def get_current_user(
    *,
    session: Session = Depends(get_session),
    token: Annotated[str, Depends(oauth2_scheme)],
) -> Any:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception

    stmt = select(User).where(
        cast("ColumnElement[bool]", User.username == token_data.username)
    )
    db_user = session.execute(stmt).scalar_one()
    if not db_user:
        raise credentials_exception
    return db_user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    # if current_user.disabled:
    # raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
