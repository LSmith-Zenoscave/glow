from sqlalchemy.orm import Session

from glow.models import url as model


def get_url(db: Session, url_id: int):
    return db.query(model.UrlModel).filter_by(id=url_id).first()


def get_by_host_path(db: Session, host: str, path: str):
    return db.query(model.UrlModel).filter_by(host=host, path=path).first()


def get_urls(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model.UrlModel).offset(skip).limit(limit).all()


def create_url(db: Session, url: model.UrlCreate):
    db_url = model.UrlModel(host=url.host, path=url.path)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url


def create_page_link(db: Session, url: model.Url, link: model.Url):
    url.links.append(link)
    db.add(url)
    db.commit()
    db.refresh(link)
    return link
