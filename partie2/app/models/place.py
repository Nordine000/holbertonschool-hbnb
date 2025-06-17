#!/usr/bin/python3
from uuid import uuid4
from datetime import datetime
from user import User

class Place:
    def __init__(self, title, price, latitude, longitude, owner, description="",created_at=None, updated_at=None, id=None):
        self.__id__ = str(uuid4())
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.__created_at__ = datetime.now()
        self.__updated_at = datetime.now()
