import pytest


@pytest.fixture
def url_server(db_connection):
    from glow.url_server import UrlServer

    return UrlServer(session=db_connection)
