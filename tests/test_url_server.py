from urllib.parse import ParseResult


class TestUrlServer:
    url_server_scenarios = (
        ["http://google.com"],
        ["https://google.com", "https://reddit.com"],
    )

    def test_get_urls(self, url_server):
        urls = url_server.list_urls()
        assert isinstance(urls, list)
        assert all(isinstance(url, dict) for url in urls)
        assert all(isinstance(url["url"], ParseResult) for url in urls)
