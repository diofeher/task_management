from typing import Union
import datetime
import enum
from sqlmodel import Field, Session, SQLModel, create_engine, Enum, Column
from sqlalchemy import DateTime
    
class TaskStatus(str, enum.Enum):
    started = "started"
    deleted = "deleted"
    finished = "finished"
    created = "created"


class TaskBase(SQLModel):
    title: str
    description: str
    due_date: datetime.datetime = Field(sa_column=Column(DateTime()))
    status: TaskStatus = Field(sa_column=Column(Enum(TaskStatus)), default=TaskStatus.created)


class Task(TaskBase, table=True):
    class Config:
        validate_assignment = True
    id: int | None = Field(default=None, primary_key=True, index=True)


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    pass

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
