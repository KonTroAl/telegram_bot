from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

from .product import Product

Base = declarative_base()

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    quantity = Column(Integer)
    date = Column(DateTime)
    product_id = Column(Integer, ForeignKey('products.id'))
    product = relationship(
        Product,
        backref=backref(
            'orders',
            uselist = True,
            cascade = 'delete, all'
        )
    )

    def __str__(self):
        return f'{self.quantity, self.date}'
