from typing import Annotated
from datetime import timedelta

from sqlmodel import Session

from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from passlib.hash import pbkdf2_sha256

from app.models.user import User, UserCreate
from app.models import get_session
from app.auth import (
    create_access_token,
    get_current_active_user,
    hash_password,
)

ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter(prefix="/users")


@router.post("/token")
async def login(
    *,
    session: Session = Depends(get_session),
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    db_user = session.get(User, form_data.username)
    if not db_user:
        raise HTTPException(
            status_code=404, detail="Incorrect username or password"
        )

    if not pbkdf2_sha256.verify(form_data.password, db_user.hashed_password):
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


@router.get("/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user


@router.post("/")
def create_user(*, session: Session = Depends(get_session), user: UserCreate):
    extra_data = {"hashed_password": hash_password(user.password)}
    db_user = User.model_validate(user, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user
