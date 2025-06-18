#!/usr/bin/python3
from uuid import uuid4
from datetime import datetime
from .user import User
from .place import Place
from .base_model import BaseModel

class Review(BaseModel):
    def __init__(self, text, place, rating=int, user=User):
        super().__init__()
        self.text = text
        self.place = place
        self.rating = rating
        self.user = user