from sqlmodel import SQLModel, Field
from sqlalchemy import Column, Integer
from pydantic import BaseModel, ConfigDict
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
    model_config = ConfigDict(validate_assignment=True)

    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
