from sqlmodel import SQLModel, Field
from sqlalchemy import Column, Integer
from pydantic import BaseModel


class User(SQLModel, table=True):
    id: int | None = Field(
        default=None,
        sa_column=Column(
            Integer, primary_key=True, nullable=True, autoincrement=True
        ),
    )
    username: str = Field(unique=True)
    hashed_password: str


class UserCreate(BaseModel):
    class Config:
        validate_assignments = True

    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
