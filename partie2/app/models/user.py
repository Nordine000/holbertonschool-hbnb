#!/usr/bin/python3
from uuid import uuid4
from datetime import datetime
from .base_model import BaseModel

class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False, created_at=None, updated_at=None, id=None):
        self.__id__ = str(uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.__created_at__ = datetime.now()
        self.__updated_at = datetime.now()
