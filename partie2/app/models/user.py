#!/usr/bin/python3
from uuid import uuid4
from datetime import datetime
from .base_model import BaseModel
import re

class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        
        """verifie l'id"""
        if not isinstance(id, str):
            raise TypeError("ID error")
        """verifie first name"""
        if not isinstance(first_name, str):
            raise ValueError("Prénom de l'user incorrect")
        if len(first_name) > 50:
            raise ValueError("Longueur max 50")
        """verifie last_name"""
        if not isinstance(last_name, str):
            raise ValueError("Nom obligatoire")
        if len(last_name) > 50:
            raise ValueError("Longueur max 50")
        """verifie l'email avec validation format"""
        if not isinstance(email, str):
            raise ValueError("L'email est obligatoire")
        regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.fullmatch(regex, email):
            raise ValueError("Format d'email non valide")
        """verifie si c'est un damin"""
        if not isinstance(is_admin, bool):
            raise TypeError("Tu n'est pas admin")
        
        
    def add_place(self, place):
        self.place.append(place)
