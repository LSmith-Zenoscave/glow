from glow.models.url import UrlModel


class TestUrlServer:
    def test_create_url(self, api_client):
        req_data = {"host": "google.com", "path": "/"}
        resp = api_client.post("/", json=req_data)
        assert resp.status_code == 200, resp.text
        resp_data = resp.json()
        assert req_data["host"] == resp_data["host"]
        assert req_data["path"] == resp_data["path"]
        assert "id" in resp_data

    def test_get_urls(self, api_client):
        resp = api_client.get("/")
        assert resp.status_code == 200, resp.text
        assert isinstance(resp.json(), list)

    def test_get_url(self, api_client, db_connection):
        req_url = UrlModel(host="test", path="/root")
        db = db_connection()
        db.add(req_url)
        db.commit()
        db.refresh(req_url)

        req_id = req_url.id
        resp = api_client.get(f"/{req_id}")
        assert resp.status_code == 200, resp.text
        assert resp.json()["id"] == req_id

        resp_422 = api_client.get(f"/invalid_id")
        assert resp_422.status_code == 422, resp_422.text

        resp_404 = api_client.get(f"/0")
        assert resp_404.status_code == 404, resp_404.text

    def test_link_url(self, api_client, db_connection):
        req_url = UrlModel(host="test", path="/root")
        db = db_connection()
        db.add(req_url)
        db.commit()
        db.refresh(req_url)

        req_link = UrlModel(host="link", path="/child", pages=[req_url])
        db.add(req_link)
        db.commit()
        db.refresh(req_link)

        req_id = req_url.id
        link_name = req_link.host + req_link.path
        resp = api_client.get(f"/{req_id}")
        assert resp.status_code == 200, resp.text

        resp_data = resp.json()
        assert resp_data["id"] == req_id
        assert link_name in (link["host"] + link["path"]
                             for link in resp_data["links"])

        resp_links = api_client.get(f"/{req_id}/links")
        assert resp_links.status_code == 200, resp_links.text
        assert link_name in (link["host"] + link["path"]
                             for link in resp_links.json())

        resp_404 = api_client.get(f"/0/links")
        assert resp_404.status_code == 404, resp.text

    def test_create_link_url(self, api_client, db_connection):
        req_url = UrlModel(host="test", path="/root")
        db = db_connection()
        db.add(req_url)
        db.commit()
        db.refresh(req_url)

        req_link = UrlModel(host="link", path="/child-nolink")
        db.add(req_link)
        db.commit()
        db.refresh(req_link)

        req_id = req_url.id
        link_id = req_link.id
        link_name = req_link.host + req_link.path
        resp = api_client.post(
            f"/{req_id}/links",
            json={
                "host": req_link.host,
                "path": req_link.path})
        assert resp.status_code == 200, resp.text

        resp_data = resp.json()
        assert resp_data["id"] == link_id

        resp_new = api_client.post(
            f"/{req_id}/links",
            json={
                "host": req_link.host,
                "path": "/new-path"})
        assert resp_new.status_code == 200, resp_new.text

        resp_new_data = resp_new.json()
        assert resp_new_data["id"] != link_id

        resp_404 = api_client.post(
            f"/0/links",
            json={
                "host": "anything",
                "path": "/anywhere"})
        assert resp_404.status_code == 404, resp_404.text
