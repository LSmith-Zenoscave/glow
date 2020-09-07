import pytest
import sqlalchemy
import glow.model

@pytest.fixture()
def db_connection():
    engine = sqlalchemy.create_engine("sqlite://")
    glow.model.Base.metadata.create_all(engine)
    Session = sqlalchemy.orm.sessionmaker()
    Session.configure(bind=engine)
    return Session()