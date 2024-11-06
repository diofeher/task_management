from sqlmodel import SQLModel, Field
from sqlalchemy import Column, Integer
from pydantic import BaseModel, ConfigDict


class User(SQLModel, table=True):  # type: ignore
    id: int | None = Field(
        default=None,
        sa_column=Column(
            Integer, primary_key=True, nullable=True, autoincrement=True
        ),
    )
    username: str = Field(unique=True)
    hashed_password: str


class UserCreate(BaseModel):  # type: ignore
    model_config = ConfigDict(validate_assignment=True)

    username: str
    password: str


class Token(BaseModel):  # type: ignore
    access_token: str
    token_type: str


class TokenData(BaseModel):  # type: ignore
    username: str | None = None
