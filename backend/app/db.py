from sqlalchemy_utils import database_exists, create_database
from sqlmodel import Session, create_engine, SQLModel
from sqlalchemy.engine import Engine
from .settings import settings


def get_engine(url: str = settings.database_url) -> Engine:
    engine = create_engine(url)
    if not database_exists(engine.url):
        create_database(engine.url)
    return engine


def get_session() -> Session:
    with Session(get_engine()) as session:
        yield session


def create_db_and_tables(engine: Engine = get_engine()) -> None:
    SQLModel.metadata.create_all(engine)


def drop_db_and_tables(engine: Engine = get_engine()) -> None:
    SQLModel.metadata.drop_all(engine)
