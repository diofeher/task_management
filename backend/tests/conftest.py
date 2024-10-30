import pytest
from fastapi.testclient import TestClient


from sqlmodel import Session, create_engine
from sqlmodel.pool import StaticPool

from app.models import (
    get_session,
    create_db_and_tables,
    drop_db_and_tables,
)
from app.main import app
from app.models.user import User
from app.auth import get_current_active_user, hash_password


def get_current_active_user_test():
    return User(
        id=100, username="rayquaza", hashed_password=hash_password("violet")
    )


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite:///test_database.db",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    create_db_and_tables(engine)
    with Session(engine) as session:
        yield session

    # import pdb;pdb.set_trace()
    drop_db_and_tables(engine)


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    app.dependency_overrides[get_current_active_user] = (
        get_current_active_user_test
    )
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
