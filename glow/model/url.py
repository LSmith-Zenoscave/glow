from glow.model.base import Base
from sqlalchemy import Column, Integer, String

class UrlModel(Base):
    __tablename__ = 'urls'

    id = Column(Integer, primary_key=True)
    host = Column(String)
    path = Column(String)