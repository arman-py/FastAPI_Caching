import os

os.environ["DATABASE_URL"] = "sqlite:///./test_cache.db"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine

from main import app
from sqlmodel import Session
from database import engine
from models import Payload, CachedTransformation


@pytest.fixture(scope="module")
def client():
    client = TestClient(app)
    yield client


@pytest.fixture(scope="module")
def session():
    with Session(engine) as session:
        yield session


@pytest.fixture(scope="module", autouse=True)
def init_db_for_tests():
    from database import init_db

    test_engine = create_engine(os.environ["DATABASE_URL"], echo=True)
    init_db()
    yield
    # Clear data after tests
    with Session(test_engine) as session:
        session.query(Payload).delete()
        session.query(CachedTransformation).delete()
        session.commit()
