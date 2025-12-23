import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.misc.database import Base, get_db
import os

SQLALCHEMY_DATABASE_URL = "postgresql://{}:{}@{}/{}".format(
    os.getenv("POSTGRES_USER", "postgres"),
    os.getenv("POSTGRES_PASSWORD", "postgres"),
    os.getenv("POSTGRES_HOST", "postgres"),
    "quotes",
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def db_engine():
    print(f"Using database URL: {SQLALCHEMY_DATABASE_URL}")
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()
    db = TestingSessionLocal(bind=connection)

    yield db

    db.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(db):
    app.dependency_overrides[get_db] = lambda: db
    with TestClient(app) as c:
        yield c
