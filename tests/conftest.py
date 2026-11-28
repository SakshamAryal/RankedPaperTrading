"""
Shared fixtures. pytest finds this file automatically, and any test can use a
fixture just by naming it as a parameter, e.g. `def test_x(client, user): ...`.

Fixtures build on each other:  engine -> db -> client / user -> auth_headers
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.config import settings
from app.dependencies.db_dependency import get_db
from app.main import app
from app.models import Base, User
from app.utils.password import hash_password

PASSWORD = "password123"


@pytest.fixture(scope="session")
def engine():
    """One engine for the whole test run. Builds the tables at start, drops them at the end."""
    url = settings.TEST_DATABASE_URL
    if not url:
        pytest.skip("TEST_DATABASE_URL is not set")
    if url == settings.DATABASE_URL:
        pytest.exit("TEST_DATABASE_URL points at the real database. Refusing to drop its tables.")

    engine = create_engine(url)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture
def db(engine):
    """
    A session wrapped in a transaction that gets rolled back after every test,
    so no test sees another test's data.

    Routes call db.commit(). With join_transaction_mode="create_savepoint", that
    commit only releases a savepoint, and the outer transaction still rolls everything back.
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection, join_transaction_mode="create_savepoint")
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db):
    """HTTP client for the app. Every route's get_db hands back the test session."""
    app.dependency_overrides[get_db] = lambda: db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def user(db):
    """A user inserted directly into the DB (we're not testing signup here)."""
    user = User(username="alice", email="alice@example.com", hashed_password=hash_password(PASSWORD))
    db.add(user)
    db.commit()
    return user


@pytest.fixture
def tokens(client, user):
    """Logs `user` in and returns the token response body."""
    response = client.post("/auth/token", data={"username": user.username, "password": PASSWORD})
    return response.json()


@pytest.fixture
def auth_headers(tokens):
    """Headers for calling protected routes as `user`."""
    return {"Authorization": f"Bearer {tokens['access_token']}"}
