from typing import Annotated, Dict
from datetime import timedelta

from sqlmodel import Session, select

from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from passlib.hash import pbkdf2_sha256

from .models import User, UserCreate
from ..db import get_session
from ..auth import (
    create_access_token,
    get_current_active_user,
    hash_password,
)

ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter(prefix="/users")


@router.post("/token")  # type: ignore
async def login(
    *,
    session: Session = Depends(get_session),
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Dict[str, str]:
    stmt = select(User).where(User.username == form_data.username)
    db_user = session.exec(stmt).first()
    if not db_user or (
        not pbkdf2_sha256.verify(form_data.password, db_user.hashed_password)
    ):
        raise HTTPException(
            status_code=400, detail="Incorrect username or password"
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.username}, expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "username": db_user.username,
        "token_type": "bearer",
    }


@router.get("/me")  # type: ignore
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> User:
    return current_user


@router.post("/")  # type: ignore
def create_user(*, session: Session = Depends(get_session), user: UserCreate):
    stmt = select(User).where(User.username == user.username)
    db_user = session.exec(stmt).first()
    if db_user:
        raise HTTPException(status_code=400, detail="User already exists")
    extra_data = {"hashed_password": hash_password(user.password)}
    db_user = User.model_validate(user, update=extra_data)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user
