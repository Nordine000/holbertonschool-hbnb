#!/usr/bin/python3
from uuid import uuid4
from datetime import datetime
from .user import User
from .base_model import BaseModel

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner.id
        self.reviews = []  # List to store related reviews
        self.amenities = []  # List to store related amenities

        """verifie le titre"""
        if not isinstance(title, str) or not title:
            raise ValueError("Titre invalide")
        if len(title) > 100:
            raise ValueError("Longueur max 100")
        """verifie description"""
        if not isinstance(description, str) or not description:
            raise ValueError("Description invalide")
        if len(description) > 50:
            raise ValueError("Longueur max 50")
        """verifie l'email avec validation format"""
        if not isinstance(price, (float, int)):
            raise TypeError("Le prix doit être un nombre")
        """verifie si c'est un la latitude"""
        if not isinstance(latitude, (float, int)):
            raise TypeError("La latitude doit etre un nombre")
        if not isinstance(longitude, (float, int)):
            raise TypeError("La longitude doit être un nombre.")
        if not isinstance(owner, User):
            raise TypeError("Le propriétaire doit être une instance de User.")

    @property
    def price(self):
        return self._price
    
    @price.setter
    def price(self, value):
        """Validate that price is a non-negative float"""
        if not isinstance(value, (int, float)):
            raise ValueError("Price must be a number")
        if value < 0:
            raise ValueError("Price must be non-negative")
        self._price = float(value)
    
    @property
    def latitude(self):
        return self._latitude
    
    @latitude.setter
    def latitude(self, value):
        """Validate that latitude is between -90 and 90"""
        if not isinstance(value, (int, float)):
            raise ValueError("Latitude must be a number")
        if not (-90 <= value <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        self._latitude = float(value)
    
    @property
    def longitude(self):
        return self._longitude
    
    @longitude.setter
    def longitude(self, value):
        """Validate that longitude is between -180 and 180"""
        if not isinstance(value, (int, float)):
            raise ValueError("Longitude must be a number")
        if not (-180 <= value <= 180):
            raise ValueError("Longitude must be between -180 and 180")
        self._longitude = float(value)
    
    def add_amenity(self, amenity_id):
        """Add an amenity to the place"""
        if amenity_id not in self.amenities:
            self.amenities.append(amenity_id)
            self.updated_at = datetime.now()
    
    def remove_amenity(self, amenity_id):
        """Remove an amenity from the place"""
        if amenity_id in self.amenities:
            self.amenities.remove(amenity_id)
            self.updated_at = datetime.now()
    
    def update(self, data):
        """Update place attributes"""
        if 'title' in data:
            self.title = data['title']
        if 'description' in data:
            self.description = data['description']
        if 'price' in data:
            self.price = data['price']  # Uses setter validation
        if 'latitude' in data:
            self.latitude = data['latitude']  # Uses setter validation
        if 'longitude' in data:
            self.longitude = data['longitude']  # Uses setter validation
        if 'amenities' in data:
            self.amenities = data['amenities']
        self.updated_at = datetime.now()
    
    def to_dict(self):
        """Convert place object to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner_id,
            'amenities': self.amenities,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f"<Place {self.id}: {self.title}>"