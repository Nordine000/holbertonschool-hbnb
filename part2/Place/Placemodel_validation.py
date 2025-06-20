# models/place.py
import uuid
from datetime import datetime

class Place:
    def __init__(self, title, description, price, latitude, longitude, owner_id, amenities=None):
        self.id = str(uuid.uuid4())
        self.title = title
        self.description = description
        self.price = price  # This will trigger the setter validation
        self.latitude = latitude  # This will trigger the setter validation
        self.longitude = longitude  # This will trigger the setter validation
        self.owner_id = owner_id
        self.amenities = amenities or []
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
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
