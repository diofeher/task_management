from sqlmodel import SQLModel, Field
from pydantic import BaseModel


class User(SQLModel, table=True):
    username: str = Field(unique=True, primary_key=True)
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
