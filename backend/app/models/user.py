from sqlmodel import SQLModel


class User(SQLModel):
    username: str
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str
