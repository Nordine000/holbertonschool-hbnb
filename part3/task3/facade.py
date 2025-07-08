#!/usr/bin/python3
"""
Extended Facade pattern implementation for all operations
"""

from persistence.repository import InMemoryRepository
from models.user import User
from models.place import Place
from models.review import Review

class HBnBFacade:
    """Facade for all HBnB operations"""
    
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
    
    # User operations
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
    
    # Place operations
    def create_place(self, place_data):
        """Create a new place"""
        place = Place(
            title=place_data['title'],
            description=place_data['description'],
            price=place_data['price'],
            latitude=place_data['latitude'],
            longitude=place_data['longitude'],
            owner_id=place_data['owner_id']
        )
        return self.place_repo.add(place)
    
    def get_place(self, place_id):
        """Get place by ID"""
        return self.place_repo.get(place_id)
    
    def get_all_places(self):
        """Get all places"""
        return self.place_repo.get_all()
    
    def get_places_by_owner(self, owner_id):
        """Get all places owned by a specific user"""
        places = self.place_repo.get_all()
        return [place for place in places if place.owner_id == owner_id]
    
    def update_place(self, place_id, place_data):
        """Update place information"""
        place = self.place_repo.get(place_id)
        if place:
            place.update(place_data)
            return self.place_repo.update(place_id, place)
        return None
    
    def delete_place(self, place_id):
        """Delete a place"""
        return self.place_repo.delete(place_id)
    
    # Review operations
    def create_review(self, review_data):
        """Create a new review"""
        review = Review(
            text=review_data['text'],
            rating=review_data['rating'],
            place_id=review_data['place_id'],
            user_id=review_data['user_id']
        )
        return self.review_repo.add(review)
    
    def get_review(self, review_id):
        """Get review by ID"""
        return self.review_repo.get(review_id)
    
    def get_all_reviews(self):
        """Get all reviews"""
        return self.review_repo.get_all()
    
    def get_reviews_by_place(self, place_id):
        """Get all reviews for a specific place"""
        reviews = self.review_repo.get_all()
        return [review for review in reviews if review.place_id == place_id]
    
    def get_reviews_by_user(self, user_id):
        """Get all reviews by a specific user"""
        reviews = self.review_repo.get_all()
        return [review for review in reviews if review.user_id == user_id]
    
    def get_user_review_for_place(self, user_id, place_id):
        """Get a user's review for a specific place"""
        reviews = self.review_repo.get_all()
        for review in reviews:
            if review.user_id == user_id and review.place_id == place_id:
                return review
        return None
    
    def update_review(self, review_id, review_data):
        """Update review information"""
        review = self.review_repo.get(review_id)
        if review:
            review.update(review_data)
            return self.review_repo.update(review_id, review)
        return None
    
    def delete_review(self, review_id):
        """Delete a review"""
        return self.review_repo.delete(review_id)

# Global facade instance
facade = HBnBFacade()
