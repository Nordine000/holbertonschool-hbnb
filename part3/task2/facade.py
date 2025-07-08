#!/usr/bin/python3
"""
Facade pattern implementation for User operations
"""

# Assuming you have a repository from previous tasks
from persistence.repository import InMemoryRepository
from models.user import User

class UserFacade:
    """Facade for user-related operations"""
    
    def __init__(self):
        self.user_repo = InMemoryRepository()
    
    def create_user(self, user_data):
        """Create a new user"""
        user = User(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            email=user_data['email'],
            password=user_data['password']
        )
        return self.user_repo.add(user)
    
    def get_user(self, user_id):
        """Get user by ID"""
        return self.user_repo.get(user_id)
    
    def get_user_by_email(self, email):
        """Get user by email address"""
        users = self.user_repo.get_all()
        for user in users:
            if user.email == email:
                return user
        return None
    
    def get_all_users(self):
        """Get all users"""
        return self.user_repo.get_all()
    
    def update_user(self, user_id, user_data):
        """Update user information"""
        user = self.user_repo.get(user_id)
        if user:
            user.update(user_data)
            return self.user_repo.update(user_id, user)
        return None
    
    def delete_user(self, user_id):
        """Delete a user"""
        return self.user_repo.delete(user_id)

# Global facade instance
facade = UserFacade()
