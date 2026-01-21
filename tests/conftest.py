from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from app.api.deps import get_db
from app.core import security
from app.db.base import Base
from app.main import app
from app.models.user import User

# Use an in-memory SQLite database for testing to ensure isolation and speed.
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    """
    Creates a fresh database session for each test.
    Create tables before test and drop them after.
    """
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session: Session) -> Generator[TestClient, None, None]:
    """
    Fixture for FastAPI TestClient with overridden DB dependency.
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def test_user(db_session: Session) -> User:
    """
    Creates a test user in the database.
    """
    user = User(
        email="testuser@example.com",
        hashed_password=security.get_password_hash("password123"),
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture(scope="function")
def auth_headers(test_user: User) -> dict:
    """
    Returns authorization headers for the test user.
    """
    access_token = security.create_access_token(subject=test_user.email)
    return {"Authorization": f"Bearer {access_token}"}