import os


class Config:
    def __init__(self, **kwargs):
        defaults = dict(
            SQLALCHEMY_DATABASE_URL="sqlite:///dev.db",
        )
        defaults.update(kwargs)
        for attr in defaults:
            setattr(self, attr, os.getenv(attr, defaults.get(attr)))


default_config = Config()
