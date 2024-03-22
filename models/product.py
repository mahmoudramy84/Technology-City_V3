#!/usr/bin/python3
""" holds class product"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship


class Product(BaseModel, Base):
    """Representation of product """
    __tablename__ = 'products'
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_pieces = Column(Integer, nullable=False, default=0)
    price = Column(Integer, nullable=False, default=0)
    reviews = relationship("Review", backref="place")


    def __init__(self, *args, **kwargs):
        """initializes Product"""
        super().__init__(*args, **kwargs)
