#!/usr/bin/python3
"""
Review model for the HBnB application.
"""
import uuid
from datetime import datetime

class Review:
    """Review class for representing reviews in the application."""
    
    def __init__(self, text, rating, place_id, user_id):
        """
        Initialize a Review instance.
        
        Args:
            text (str): Review text content
            rating (int): Rating from 1 to 5
            place_id (str): ID of the place being reviewed
            user_id (str): ID of the user who wrote the review
        """
        self.id = str(uuid.uuid4())
        self.text = text
        self.rating = int(rating)
        self.place_id = place_id
        self.user_id = user_id
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def to_dict(self):
        """
        Convert Review instance to dictionary representation.
        
        Returns:
            dict: Dictionary representation of review
        """
        return {
            'id': self.id,
            'text': self.text,
            'rating': self.rating,
            'place_id': self.place_id,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def update(self, data):
        """
        Update review attributes.
        
        Args:
            data (dict): Dictionary containing fields to update
        """
        for key, value in data.items():
            if hasattr(self, key) and key not in ['id', 'place_id', 'user_id', 'created_at']:
                if key == 'rating':
                    setattr(self, key, int(value))
                else:
                    setattr(self, key, value)
        
        self.updated_at = datetime.now()
    
    def __repr__(self):
        """String representation of Review."""
        return f"<Review {self.id}: {self.rating}/5 for Place {self.place_id}>"
