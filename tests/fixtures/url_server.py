import pytest


@pytest.fixture
def url_server(request):
    from glow.url_server import UrlServer

    return UrlServer(request.param)
