import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.database.db import get_session
from app.main import app


# Create in-memory SQLite database for testing
@pytest.fixture
def test_db_engine():
    # Use in-memory SQLite database for tests
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    return engine


@pytest.fixture
def test_session(test_db_engine):
    with Session(test_db_engine) as session:
        yield session


@pytest.fixture
def client(test_db_engine, test_session):
    # Override get_session with our test session
    def get_test_session():
        return test_session

    app.dependency_overrides[get_session] = get_test_session

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()
