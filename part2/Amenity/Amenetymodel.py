# models/amenity.py
import uuid
from datetime import datetime

class Amenity:
    def __init__(self, name):
        self.id = str(uuid.uuid4())
        self.name = name
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
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
        """Update amenity attributes"""
        if 'name' in data:
            self.name = data['name']
        self.updated_at = datetime.now()
