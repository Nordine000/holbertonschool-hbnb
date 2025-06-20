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
        self.owner = owner
        self.reviews = []  # List to store related reviews
        self.amenities = []  # List to store related amenities

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

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)