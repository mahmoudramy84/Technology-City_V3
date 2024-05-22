#!/usr/bin/python3
""" holds class User"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash

class User(BaseModel, Base):
    """Representation of a user """
    
    __tablename__ = 'users'
    email = Column(String(128), nullable=False)
    password = Column(String(512), nullable=False)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)

    reviews = relationship("Review", backref="author", cascade="all, delete-orphan")
    products = relationship("Product", backref='user', foreign_keys='Product.user_id', primaryjoin="User.id==Product.user_id")
    cart_items = relationship("Cart", back_populates="user", cascade="all, delete-orphan")

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)
"""        if 'password' in kwargs:
            self.password = generate_password_hash(kwargs['password'])"""
