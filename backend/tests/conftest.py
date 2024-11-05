import pytest
import os
from fastapi.testclient import TestClient


from sqlmodel import Session

from app.main import app
from backend.app.users.models import User
from app.auth import get_current_active_user, hash_password
from app.db import (
    get_engine,
    get_session,
    create_db_and_tables,
    drop_db_and_tables,
)

# TODO: Hardcoded for now, pass as configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://myuser:mypassword@localhost:5432/testdatabase",
)


@pytest.fixture(name="session")
def session_fixture():
    engine = get_engine(DATABASE_URL)

    create_db_and_tables(engine)
    with Session(engine) as session:
        yield session

    drop_db_and_tables(engine)


@pytest.fixture(name="current_user")
def current_user_fixture(session):
    current_user = User(
        id=100, username="rayquaza", hashed_password=hash_password("violet")
    )
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    yield current_user


@pytest.fixture(name="client")
def client_fixture(current_user, session: Session):
    def get_session_override():
        return session

    def get_current_active_user_test():
        return current_user

    app.dependency_overrides[get_session] = get_session_override
    app.dependency_overrides[get_current_active_user] = (
        get_current_active_user_test
    )
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
