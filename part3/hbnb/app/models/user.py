#!/usr/bin/python3
from uuid import uuid4
from datetime import datetime
from .base_model import BaseModel
import re
from app.__init__ import bcrypt
from app import db, bcrypt


class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    place_list = db.relationship('Place', backref='owner', lazy=True)
    review_list = db.relationship('Review', backref='author', lazy=True)
    
    def __init__(self, first_name, last_name, email, is_admin=False, id=None):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.password = None
        self.email = email
        self.is_admin = is_admin
        if id:
            self.id = id
        

    def validate_user(self):
        """Validate user informations format"""
        if not self.first_name:
            raise ValueError("First name is required")
        if not self.last_name:
            raise ValueError("Last name is required")
        if not self.email:
            raise ValueError("Email is required")
        if not self.password:
            raise ValueError("Password is required")
        #email validation
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, self.email):
            raise ValueError("Invalid email format")


    
    def update(self, data):
        """Update user attributes"""
        if 'first_name' in data:
            self.first_name = data['first_name']
        if 'last_name' in data:
            self.last_name = data['last_name']
        if 'email' in data:
            self.email = data['email']  # Uses setter validation
        self.updated_at = datetime.now()
    
    def to_dict(self):
        """Convert user object to dictionary"""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),}
    
    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)
