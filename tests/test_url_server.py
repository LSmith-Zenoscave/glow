from urllib.parse import ParseResult
from glow.model import Url


class TestUrlServer:
    def test_insert_urls(self, url_server):
        url = url_server.insert_url(host="facebook.com", path="me")
        assert isinstance(url, Url)

    def test_get_urls(self, url_server):
        url = url_server.insert_url(host="google.com", path="/")
        urls = url_server.list_urls()
        assert isinstance(urls, list)
        assert all(isinstance(url, Url) for url in urls)
        assert url in urls