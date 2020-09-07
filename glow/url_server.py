from urllib.parse import urlparse


class UrlServer:
    def __init__(self, urls):
        self.urls = [
            {"url": urlparse(url)}
            for url in urls
        ]

    def list_urls(self):
        return self.urls
