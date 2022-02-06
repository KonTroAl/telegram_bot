from os import path
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from settings import settings
from settings.utility import _convert
from .dbcore import Base
from models.product import Product
from models.order import Order


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
        Session = sessionmaker(bind=self.engine)
        self._session = Session()
        if not path.isfile(settings.DATABASE):
            Base.metadata.create_all(self.engine)

    def select_all_product_category(self, category):
        result = self._session.query(Product).filter_by(category_id=category).all()
        self.close()
        return result

    def close(self):
        self._session.close()

    def _add_orders(self, quantity, product_id, user_id):

        all_products_id = self.select_all_products_id()

        if product_id in all_products_id:
            order_quantity = self.select_order_quantity(product_id)
            order_quantity += 1
            self.update_order_value(product_id, 'quantity', order_quantity)

            product_quantity = self.select_single_product_quantity(product_id)
            product_quantity -= 1
            self.update_product_value(product_id, 'quantity', product_quantity)
            return
        else:
            order = Order(quantity=quantity, product_id=product_id,
                          user_id=user_id, date=datetime.now())
            product_quantity = self.select_single_product_quantity(product_id)
            product_quantity -= 1
            self.update_product_value(product_id, 'quantity', product_quantity)

        self._session.add(order)
        self._session.commit()
        self.close()

    def select_all_products_id(self):
        result = self._session.query(Order.product_id).all()
        self.close()
        return _convert(result)

    def select_order_quantity(self, product_id):
        result = self._session.query(Order.quantity).filter_by(product_id=product_id).one()
        self.close()
        return result.quantity

    def update_order_value(self, product_id, name, value):
        self._session.query(Order).filter_by(product_id=product_id).update({name: value})
        self._session.commit()
        self.close()

    def update_product_value(self, product_id, name, value):
        self._session.query(Product).filter_by(
            id=product_id).update({name: value})
        self._session.commit()
        self.close()

    def select_single_product_name(self, product_id):
        result = self._session.query(Product.name).filter_by(id=product_id).one()
        self.close()
        return result.name

    def select_single_product_title(self, product_id):
        result = self._session.query(Product.title).filter_by(id=product_id).one()
        self.close()
        return result.title

    def select_single_product_price(self, product_id):
        result = self._session.query(Product.price).filter_by(id=product_id).one()
        self.close()
        return result.price

    def select_single_product_quantity(self, product_id):
        result = self._session.query(Product.quantity).filter_by(id=product_id).one()
        self.close()
        return result.quantity

    def count_row_orders(self):
        result = self._session.query(Order).count()
        self.close()
        return result

    def delete_order(self, product_id):
        self._session.query(Order).filter_by(product_id=product_id).delete()
        self._session.commit()
        self.close()

    def delete_all_order(self):
        all_id_orders = self.select_all_order_id()
        for itm in all_id_orders:
            self._session.query(Order).filter_by(id=itm).delete()
            self._session.commit()
        self.close()

    def select_all_order_id(self):
        result = self._session.query(Order.id).all()
        self.close()
        return _convert(result)
