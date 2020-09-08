from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from glow.controllers import url as controller
from glow.database import Base, init_db
from glow.models import url as model
from glow.config import default_config
from sqlalchemy.exc import IntegrityError

engine, SessionLocal = init_db(default_config)
Base.metadata.create_all(bind=engine)


def get_db():  # pragma: no cover ## Overridden in test-db.
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()


@app.post("/", response_model=model.Url)
def create_url(url: model.UrlCreate, db: Session = Depends(get_db)):
    return controller.create_url(db, url=url)


@app.get("/", response_model=List[model.Url])
def get_urls(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    urls = controller.get_urls(db, skip=skip, limit=limit)
    return urls


@app.get("/{url_id}", response_model=model.Url)
def get_url(url_id: int, db: Session = Depends(get_db)):
    url = controller.get_url(db, url_id=url_id)
    if url is None:
        raise HTTPException(status_code=404, detail="Url not found")
    return url


@app.post("/{url_id}/links", response_model=model.Url)
def create_link_for_page(
        url_id: int,
        link: model.UrlCreate,
        db: Session = Depends(get_db)):
    url = controller.get_url(db, url_id=url_id)
    if url is None:
        raise HTTPException(status_code=404, detail="Url not found")
    link_url = controller.get_by_host_path(db, host=link.host, path=link.path)
    if link_url is None:
        link_url = controller.create_url(db, link)
    return controller.create_page_link(db, url, link_url)


@app.get("/{url_id}/links", response_model=List[model.Url])
def get_links_for_page(url_id: int, db: Session = Depends(get_db)):
    url = controller.get_url(db, url_id=url_id)
    if url is None:
        raise HTTPException(status_code=404, detail="Url not found")
    return url.links
