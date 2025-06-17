#!/usr/bin/python3
from uuid import uuid4
from datetime import datetime
from base_model import BaseModel

class Amenity(BaseModel):
    def __init__(self, name, created_at=None, updated_at=None, id=None):
        self.id = str(uuid4())
        self.name = name
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
