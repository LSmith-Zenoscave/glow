from urllib.parse import urlparse
from glow.model import Url

class UrlServer:
    def __init__(self, session):
        self.session = session

    def insert_url(self, host, path):
        url = Url(host=host, path=path)
        self.session.add(url)
        self.session.commit()
        return url

    def list_urls(self):
        return list(self.session.query(Url))
