from sqlmodel import Session, create_engine, SQLModel
from .task import Task, TaskUpdate, TaskCreate, TaskStatus
from .user import User, UserInDB

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables(eng=engine):
    SQLModel.metadata.create_all(eng)


def drop_db_and_tables(eng=engine):
    SQLModel.metadata.drop_all(eng)


def get_session():
    with Session(engine) as session:
        yield session


__all__ = [
    "Task",
    "TaskUpdate",
    "TaskCreate",
    "TaskStatus",
    "User",
    "UserInDB",
]
