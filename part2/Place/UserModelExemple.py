# models/user.py
# This is an example of what your User model might look like
# You should already have this from previous tasks

import uuid
from datetime import datetime

class User:
    def __init__(self, first_name, last_name, email):
        self.id = str(uuid.uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
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
    
    def to_dict(self):
        """Convert user object to dictionary"""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
