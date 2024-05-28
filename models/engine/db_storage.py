#!/usr/bin/python3
"""
Contains the class DBStorage
"""

from models.base_model import Base
from models.product import Product
from models.review import Review
from models.user import User
from models.cart import Cart
from dotenv import load_dotenv
from  os  import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.pool import QueuePool
from contextlib import contextmanager

#from urllib.parse import quote_plus

classes = {"User": User, "Product": Product, "Review": Review, "Cart": Cart}

class DBStorage:
    """Interacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        tech_MYSQL_USER = getenv('tech_MYSQL_USER')
        tech_MYSQL_PWD = getenv('tech_MYSQL_PWD')
        tech_MYSQL_HOST = getenv('tech_MYSQL_HOST')
        tech_MYSQL_DB = getenv('tech_MYSQL_DB')
        tech_ENV = getenv('tech_ENV')
        self.__engine = create_engine(
            f'mysql+mysqldb://{tech_MYSQL_USER}:{tech_MYSQL_PWD}@{tech_MYSQL_HOST}/{tech_MYSQL_DB}',
            poolclass=QueuePool,
            pool_size=10,            # Increase pool size
            max_overflow=20,         # Increase max overflow
            pool_timeout=30          # Set timeout
        )
        if tech_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query on the current database session"""
        new_dict = {}
        with self.__session() as session:
            for clss in classes:
                if cls is None or cls is classes[clss] or cls is clss:
                    objs = session.query(classes[clss]).all()
                    for obj in objs:
                        key = obj.__class__.__name__ + '.' + obj.id
                        new_dict[key] = obj
        return new_dict

    def new(self, obj):
        """Add the object to the current database session"""
        with self.__session() as session:
            session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        with self.__session() as session:
            session.commit()

    def delete(self, obj=None):
        """Delete from the current database session obj if not None"""
        if obj is not None:
            with self.__session() as session:
                session.delete(obj)

    def reload(self):
        """Reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(sess_factory)

    def close(self):
        """Call remove() method on the private session attribute"""
        self.__session.remove()

    def get(self, cls, id):
        """Retrieve an object by class and ID"""
        with self.__session() as session:
            return session.query(cls).get(id)

    @contextmanager
    def session_scope(self):
        """Provide a transactional scope around a series of operations."""
        session = self.__session()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
