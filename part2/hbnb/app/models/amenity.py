#!/usr/bin/python3
from uuid import uuid4
from datetime import datetime
from .base_model import BaseModel

class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        self.name = name
        """verifie le nom si str et garantit que la chaine contient un char"""
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Le nom de l'équipement doit être une chaîne non vide.")
        if len(name) > 100:
            raise ValueError("Le nom ne peut pas dépasser 100 caractères.")