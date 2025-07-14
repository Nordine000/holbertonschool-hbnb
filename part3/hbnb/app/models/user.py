#!/usr/bin/python3
from uuid import uuid4
from datetime import datetime
from .base_model import BaseModel
import re
from app import bcrypt

class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False, id=None, password=None):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self._email = None
        self.email = email
        self.is_admin = is_admin
        self.place = []
        self._password = None
        self.id = id or str(uuid4())

            # Hash password if provided
        if password:
            self.hash_password(password)
        
        
        
        """verifie l'id"""
        if id is not None and not isinstance(id, str):
            raise TypeError("id doit être une chaîne de caractères")
        """verifie first name"""
        if not isinstance(first_name, str):
            raise ValueError("Prénom de l'user incorrect")
        if len(first_name) > 50:
            raise ValueError("Longueur max 50")
        """verifie last_name"""
        if not isinstance(last_name, str):
            raise ValueError("Nom obligatoire")
        if len(last_name) > 50:
            raise ValueError("Longueur max 50")
        """verifie l'email avec validation format"""
        if not isinstance(email, str):
            raise ValueError("L'email est obligatoire")
        regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.fullmatch(regex, email):
            raise ValueError("Format d'email non valide")
        """verifie si c'est un damin"""
        if not isinstance(is_admin, bool):
            raise TypeError("Tu n'est pas admin")
        
        
    def add_place(self, place):
        self.place.append(place)
    
    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, value):
        """Validate email format"""
        import re
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, value):
            raise ValueError("Invalid email format")
        self._email = value
    
    def update(self, data):
        """Update user attributes"""
        if 'first_name' in data:
            self.first_name = data['first_name']
        if 'last_name' in data:
            self.last_name = data['last_name']
        if 'email' in data:
            self.email = data['email']  # Uses setter validation
        self.updated_at = datetime.now()

        for key, value in data.items():
            if key == 'password':
                # Hash password if it's being updated
                self.hash_password(value)
            elif hasattr(self, key) and key not in ['id', 'created_at']:
                setattr(self, key, value)

        self.updated_at = datetime.now()

    def __repr__(self):
        """String representation of User."""
        return f"<User {self.id}: {self.email}>"

    def to_dict(self, include_password=False):
        """Convert user object to dictionary"""
        user_dict = {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        
        # Only include password if explicitly requested (for internal use)
        if include_password and self._password:
            user_dict['password'] = self._password
            
        return user_dict
    
    def hash_password(self, password):
        self._password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def verify_password(self, password):
        return bcrypt.check_password_hash(self._password, password)