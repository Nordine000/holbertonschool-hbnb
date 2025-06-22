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


        """verifie le texte"""
        if not isinstance(text, str) or not text.strip():
            raise ValueError("Le commentaire doit être une chaîne de caractères non vide.")
        if len(text) > 1000:
            raise ValueError("Le commentaire ne peut pas dépasser 1000 caractères.")
        """verifie le lieu"""
        if not isinstance(place, Place):
            raise TypeError("Le lieu doit être une instance de Place.")
        """veirifie l'uyilisteur"""
        if not isinstance(user, User):
            raise TypeError("L'utilisateur doit être une instance de User.")
        """verifie la note max 5 etoile"""
        if not isinstance(rating, (int, float)):
            raise TypeError("La note doit être un nombre.")
        if not (0 <= rating <= 5):
            raise ValueError("La note doit être comprise entre 0 et 5.")
