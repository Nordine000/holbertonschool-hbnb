#!/usr/bin/python3
"""
User model for the HBnB application with admin support.
"""
import uuid
from datetime import datetime
from app import bcrypt

class User:
    """User class for representing users in the application."""
    
    def __init__(self, first_name, last_name, email, password=None, is_admin=False):
        """
        Initialize a User instance.
        
        Args:
            first_name (str): User's first name
            last_name (str): User's last name  
            email (str): User's email address
            password (str, optional): User's plaintext password
            is_admin (bool, optional): Whether user has admin privileges
        """
        self.id = str(uuid.uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = None  # Will store hashed password
        self.is_admin = is_admin
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        
        # Hash password if provided
        if password:
            self.hash_password(password)
    
    def hash_password(self, password):
        """
        Hashes the password before storing it.
        
        Args:
            password (str): Plaintext password to hash
        """
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def verify_password(self, password):
        """
        Verifies if the provided password matches the hashed password.
        
        Args:
            password (str): Plaintext password to verify
            
        Returns:
            bool: True if password matches, False otherwise
        """
        return bcrypt.check_password_hash(self.password, password)
    
    def to_dict(self, include_password=False):
        """
        Convert User instance to dictionary representation.
        
        Args:
            include_password (bool): Whether to include password in output
            
        Returns:
            dict: Dictionary representation of user
        """
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
        if include_password and self.password:
            user_dict['password'] = self.password
            
        return user_dict
    
    def update(self, data):
        """
        Update user attributes.
        
        Args:
            data (dict): Dictionary containing fields to update
        """
        for key, value in data.items():
            if key == 'password':
                # Hash password if it's being updated
                self.hash_password(value)
            elif key == 'email':
                # Update email (admin can change this)
                self.email = value
            elif key == 'is_admin':
                # Update admin status (only admins should be able to do this)
                self.is_admin = bool(value)
            elif hasattr(self, key) and key not in ['id', 'created_at']:
                setattr(self, key, value)
        
        self.updated_at = datetime.now()
    
    def __repr__(self):
        """String representation of User."""
        admin_str = " (Admin)" if self.is_admin else ""
        return f"<User {self.id}: {self.email}{admin_str}>"
