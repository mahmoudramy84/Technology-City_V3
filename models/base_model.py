#!/usr/bin/python3
"""
Contains class BaseModel
"""

from datetime import datetime
import models
from os import getenv
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import uuid

time = "%Y-%m-%dT%H:%M:%S.%f"

Base = declarative_base()


class BaseModel:
    """The BaseModel class from which future classes will be derived"""
    id = Column(String(60), primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Initialization of the base model"""
        self.id = Column(String(60), primary_key=True)
        self.created_at = Column(DateTime, default=datetime.utcnow)
        self.updated_at = Column(DateTime, default=datetime.utcnow)

        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)

            self.created_at = self.parse_datetime(kwargs.get("created_at", datetime.utcnow()))
            self.updated_at = self.parse_datetime(kwargs.get("updated_at", datetime.utcnow()))

            if not kwargs.get("id"):
                self.id = str(uuid.uuid4())
            

    def __str__(self):
        """String representation of the BaseModel class"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
                                         self.__dict__)

    def save(self):
        """updates the attribute 'updated_at' with the current datetime"""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def parse_datetime(self, dt_str):
        try:
            return datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S.%f")
        except (TypeError, ValueError):
            return datetime.utcnow()

    def to_dict(self):
        """returns a dictionary containing all keys/values of the instance"""
        new_dict = {}
        for key, value in self.__dict__.items():
            if key != "_sa_instance_state":
                if isinstance(value, datetime):
                    new_dict[key] = value.strftime("%Y-%m-%d %H:%M:%S.%f")
                else:
                    new_dict[key] = value
        return new_dict
