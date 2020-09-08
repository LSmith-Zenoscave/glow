import pytest
from fastapi.testclient import TestClient
from glow.url_server import app, get_db
from glow.database import Base


@pytest.fixture
def api_client(db_connection):
    db = db_connection()
    meta = Base.metadata
    meta.drop_all(bind=db.get_bind(), checkfirst=False)
    meta.create_all(bind=db.get_bind())

    def override_db():
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_db
    return TestClient(app)
