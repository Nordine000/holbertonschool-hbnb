from .base_model import BaseModel
from uuid import uuid4
from app import db
from datetime import datetime
from .user import User
from .place import Place



class Review(BaseModel):
    """represents a Review tied to Place by Composition and dependent on User"""
    __tablename__ = 'reviews'
    
    text = db.Column(db.String(500), nullable=True)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)


    def __init__(self, text, place, rating, user):
        super().__init__()
        self.text = text
        self.place_id = place.id
        self.rating = float(rating)
        self.user_id = user.id
        self.validate_review()


        """verifie le texte"""
        if not isinstance(text, str) or not text.strip():
            raise ValueError("Le commentaire doit être une chaîne de caractères non vide.")
        if len(text) > 1000:
            raise ValueError("Le commentaire ne peut pas dépasser 1000 caractères.")
        """verifie le lieu"""
        if not isinstance(place, Place):
            raise TypeError("Le lieu doit être une instance de Place.")
        """veirifie l'uyilisteur"""
        if not isinstance(user, User):
            raise TypeError("L'utilisateur doit être une instance de User.")
        """verifie la note max 5 etoile"""
        if not isinstance(rating, (int, float)):
            raise TypeError("La note doit être un nombre.")
        if not (0 <= rating <= 5):
            raise ValueError("La note doit être comprise entre 0 et 5.")
        
    def validate_review(self):
        """Validates review informations format"""

        if not isinstance(self.text, str) or not self.text.strip():
            raise ValueError("Text is required and must be a non-empty string")
        if not isinstance(self.rating, int) or not (1 <= self.rating <= 5):
            raise ValueError("Rating must be an integer between 1 and 5")
