import os
from sqlalchemy_utils import database_exists, create_database
from sqlmodel import Session, create_engine, SQLModel
from app.settings import settings


def get_engine(url=settings.database_url):
    engine = create_engine(url)
    if not database_exists(engine.url):
        create_database(engine.url)
    return engine


def get_session():
    with Session(get_engine()) as session:
        yield session


def create_db_and_tables(engine):
    SQLModel.metadata.create_all(engine)


def drop_db_and_tables(engine):
    SQLModel.metadata.drop_all(engine)
