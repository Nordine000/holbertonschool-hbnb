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


        """verifie le titre"""
        if not isinstance(title, str) or not title:
            raise ValueError("Titre du lieu")
        if len(title) > 100:
            raise ValueError("Longueur max 100")
        """verifie description"""
        if not isinstance(description, str) or not description:
            raise ValueError("Nom obligatoire")
        if len(description) > 50:
            raise ValueError("Longueur max 50")
        """verifie l'email avec validation format"""
        if not isinstance(price, float):
            raise TypeError("L'email est obligatoire")
        """verifie si c'est un damin"""
        if not isinstance(latitude, float):
            raise TypeError("Tu n'est pas admin")
