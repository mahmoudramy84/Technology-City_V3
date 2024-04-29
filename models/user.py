#!/usr/bin/python3
""" holds class User"""
from models.base_model import BaseModel, Base
from models.product import Product
from os import getenv
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash



class User(BaseModel, Base):
    """Representation of a user """
    
    __tablename__ = 'users'
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)

    # One-to-Many relationship: One user can have many reviews
    reviews = relationship("Review", backref="author")

    # Many-to-Many relationship: Users can have many products and vice versa
    products = relationship("Product", backref='user', foreign_keys=[Product.user_id], primaryjoin="User.id==Product.user_id")

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)

        if 'password' in kwargs:
            # Hash the password before storing it
            self.password = generate_password_hash(kwargs['password'])

"""
    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, pwd):
        self._password = hashlib.md5(pwd.encode()).hexdigest()
"""
