
from typing import List, ForwardRef
from glow.database import Base
from sqlalchemy import Column, ForeignKey, Integer, Table, String, UniqueConstraint
from sqlalchemy.orm import relationship, backref
from pydantic import BaseModel

page_link = Table(
    'page_link',
    Base.metadata,
    Column('page_id', Integer, ForeignKey('urls.id'),
           primary_key=True),
    Column('link_id', Integer, ForeignKey('urls.id'),
           primary_key=True)
)


class UrlModel(Base):
    __tablename__ = 'urls'
    __table_args__ = (
        UniqueConstraint('host', 'path', name='_host_path_uc'),
    )
    id = Column(Integer, primary_key=True)
    host = Column(String)
    path = Column(String)
    links = relationship(
        "UrlModel",
        secondary=page_link,
        primaryjoin=id == page_link.c.link_id,
        secondaryjoin=id == page_link.c.page_id,
        backref=backref('pages')
    )


class UrlBase(BaseModel):
    host: str
    path: str

    class Config:
        orm_mode = True


class UrlCreate(UrlBase):
    pass


Url = ForwardRef('Url')


class Url(UrlBase):
    id: int
    links: List[UrlBase] = []
    pages: List[UrlBase] = []

    class Config:
        orm_mode = True


Url.update_forward_refs()
