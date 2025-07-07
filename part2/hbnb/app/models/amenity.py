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
        
    def __repr__(self):
        return f"<Amenity {self.id}: {self.name}>"
    
    def to_dict(self):
        """Convert amenity object to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def update(self, data):
        """Update amenity attributes with validation"""
        if 'name' in data:
            name = data['name']
            if not isinstance(name, str) or not name.strip():
                raise ValueError("Le nom de l'équipement doit être une chaîne non vide.")
            if len(name) > 100:
                raise ValueError("Le nom ne peut pas dépasser 100 caractères.")
            self.name = name
            self.updated_at = datetime.now()
