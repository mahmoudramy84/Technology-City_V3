#!/usr/bin/python3
""" holds class product"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

class Product(BaseModel, Base):
    """Representation of product """
    __tablename__ = 'products'
    user_id = Column(String(60), ForeignKey('users.id'))
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_pieces = Column(Integer, nullable=True, default=0)
    price = Column(Float, nullable=False, default=0.0)
    image_url = Column(String(512), nullable=True)
    category = Column(String(128), nullable=True)

    # One-to-Many relationship: One product can have many reviews
    reviews = relationship("Review", backref="product", cascade="all, delete-orphan")

    def __init__(self, *args, **kwargs):
        """initializes Product"""
        super().__init__(*args, **kwargs)
