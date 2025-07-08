#!/usr/bin/python3
"""
Amenity model for the HBnB application.
"""
import uuid
from datetime import datetime

class Amenity:
    """Amenity class for representing amenities in the application."""
    
    def __init__(self, name):
        """
        Initialize an Amenity instance.
        
        Args:
            name (str): Amenity name
        """
        self.id = str(uuid.uuid4())
        self.name = name
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def to_dict(self):
        """
        Convert Amenity instance to dictionary representation.
        
        Returns:
            dict: Dictionary representation of amenity
        """
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def update(self, data):
        """
        Update amenity attributes.
        
        Args:
            data (dict): Dictionary containing fields to update
        """
        for key, value in data.items():
            if hasattr(self, key) and key not in ['id', 'created_at']:
                setattr(self, key, value)
        
        self.updated_at = datetime.now()
    
    def __repr__(self):
        """String representation of Amenity."""
        return f"<Amenity {self.id}: {self.name}>"
