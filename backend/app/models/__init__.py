from sqlmodel import Session, create_engine, SQLModel

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
