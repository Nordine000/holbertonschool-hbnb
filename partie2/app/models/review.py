#!/usr/bin/python3
from uuid import uuid4
from datetime import datetime
from .user import User
from .place import Place
from .base_model import BaseModel

class Review(BaseModel):
    def __init__(self, text, place, rating=int, user=User,created_at=None, updated_at=None, id=None):
        self.__id__ = str(uuid4())
        self.text = text
        self.place = place
        self.rating = rating
        self.user = user
        self.__created_at__ = datetime.now()
        self.__updated_at = datetime.now()