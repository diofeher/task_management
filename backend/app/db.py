import os
from sqlalchemy_utils import database_exists, create_database
from sqlmodel import Session, create_engine, SQLModel

# TODO: Remove hardcoded, Pass by config
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://myuser:mypassword@db:5432/mydatabase")

def get_engine(url=DATABASE_URL):
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



