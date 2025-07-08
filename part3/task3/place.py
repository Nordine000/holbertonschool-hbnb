#!/usr/bin/python3
"""
Place model for the HBnB application.
"""
import uuid
from datetime import datetime

class Place:
    """Place class for representing places in the application."""
    
    def __init__(self, title, description, price, latitude, longitude, owner_id):
        """
        Initialize a Place instance.
        
        Args:
            title (str): Place title
            description (str): Place description
            price (float): Price per night
            latitude (float): Geographic latitude
            longitude (float): Geographic longitude
            owner_id (str): ID of the user who owns this place
        """
        self.id = str(uuid.uuid4())
        self.title = title
        self.description = description
        self.price = float(price)
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.owner_id = owner_id
        self.amenities = []  # List of amenity IDs
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def to_dict(self):
        """
        Convert Place instance to dictionary representation.
        
        Returns:
            dict: Dictionary representation of place
        """
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
    
    def update(self, data):
        """
        Update place attributes.
        
        Args:
            data (dict): Dictionary containing fields to update
        """
        for key, value in data.items():
            if hasattr(self, key) and key not in ['id', 'owner_id', 'created_at']:
                if key in ['price', 'latitude', 'longitude']:
                    setattr(self, key, float(value))
                else:
                    setattr(self, key, value)
        
        self.updated_at = datetime.now()
    
    def add_amenity(self, amenity_id):
        """Add an amenity to the place."""
        if amenity_id not in self.amenities:
            self.amenities.append(amenity_id)
    
    def remove_amenity(self, amenity_id):
        """Remove an amenity from the place."""
        if amenity_id in self.amenities:
            self.amenities.remove(amenity_id)
    
    def __repr__(self):
        """String representation of Place."""
        return f"<Place {self.id}: {self.title}>"
