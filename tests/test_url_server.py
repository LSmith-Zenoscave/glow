import pytest

@pytest.fixture
def url_server():
    from glow.url_server import UrlServer

    return UrlServer()


class TestUrlServer:
    def test_get_urls(self, url_server):
        assert True