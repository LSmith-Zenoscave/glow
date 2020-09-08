import pytest
from glow.database import Base, init_db
from glow.config import Config

engine, TestingSessionLocal = init_db(
    Config(SQLALCHEMY_DATABASE_URL="sqlite:///test.db")
)

Base.metadata.create_all(bind=engine)


@pytest.fixture()
def db_connection():
    return TestingSessionLocal
