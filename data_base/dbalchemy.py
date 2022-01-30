from os import path

from sqlalchemy import create_engine
from sqlalchemy.orm import create_session

from settings import settings
from .dbcore import Base
from models.product import Product


class Singleton(type):

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = None

    def __call__(cls, *args, **kwargs):
        if cls.__instance == None:
            cls.__instance = super().__call__(*args, **kwargs)
        return cls.__instance


class DBManager(metaclass=Singleton):
    def __init__(self):
        self.engine = create_engine(settings.DATABASE)
        session = create_session(bind=self.engine)
        self._session = session
        if not path.isfile(settings.DATABASE):
            Base.metadata.create_all(self.engine)

    def select_all_product_category(self, category):
        result = self._session.query(Product).filter_by(category_id=category).all()
        self.close()
        return result

    def close(self):
        self._session.close()

