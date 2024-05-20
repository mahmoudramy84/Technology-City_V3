#!/usr/bin/python3
"""Holds class Cart"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship

class Cart(BaseModel, Base):
    """Representation of a cart"""
    __tablename__ = 'carts'
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    product_id = Column(String(60), ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)

    user = relationship("User", back_populates="cart_items")
    product = relationship("Product")

    def __init__(self, *args, **kwargs):
        """Initializes Cart"""
        super().__init__(*args, **kwargs)
