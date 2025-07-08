#!/usr/bin/python3
"""
HBnB Facade with SQLAlchemy Repository Integration
"""

from app.persistence.repository import SQLAlchemyRepository
# Note: These imports will work once models are mapped in the next task
# from app.models.user import User
# from app.models.place import Place
# from app.models.review import Review
# from app.models.amenity import Amenity

class HBnBFacade:
    """
    Facade pattern implementation for HBnB operations using SQLAlchemy
    """
    
    def __init__(self):
        """
        Initialize the facade with SQLAlchemy repositories
        Note: Model imports are commented until next task when models are mapped
        """
        # These will be uncommented once models are mapped to SQLAlchemy
        # self.user_repo = SQLAlchemyRepository(User)
        # self.place_repo = SQLAlchemyRepository(Place)
        # self.review_repo = SQLAlchemyRepository(Review)
        # self.amenity_repo = SQLAlchemyRepository(Amenity)
        
        # Temporary: Use in-memory repositories until models are mapped
        from app.persistence.repository import InMemoryRepository
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
    
    # USER OPERATIONS
    def create_user(self, user_data):
        """
        Create a new user
        
        Args:
            user_data (dict): User data dictionary
            
        Returns:
            User: Created user instance
        """
        # Note: This will be updated once User model is mapped
        # user = User(**user_data)
        # return self.user_repo.add(user)
        
        # Temporary implementation using existing User class
        from models.user import User
        user = User(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            email=user_data['email'],
            password=user_data.get('password')
        )
        
        if 'is_admin' in user_data:
            user.is_admin = user_data['is_admin']
            
        return self.user_repo.add(user)
    
    def get_user(self, user_id):
        """Get user by ID"""
        return self.user_repo.get(user_id)
    
    def get_user_by_email(self, email):
        """Get user by email address"""
        return self.user_repo.get_by_attribute('email', email)
    
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
    
    # PLACE OPERATIONS
    def create_place(self, place_data):
        """Create a new place"""
        # Note: This will be updated once Place model is mapped
        from models.place import Place
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
    
    # REVIEW OPERATIONS
    def create_review(self, review_data):
        """Create a new review"""
        from models.review import Review
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
    
    # AMENITY OPERATIONS
    def create_amenity(self, amenity_data):
        """Create a new amenity"""
        from models.amenity import Amenity
        amenity = Amenity(name=amenity_data['name'])
        return self.amenity_repo.add(amenity)
    
    def get_amenity(self, amenity_id):
        """Get amenity by ID"""
        return self.amenity_repo.get(amenity_id)
    
    def get_all_amenities(self):
        """Get all amenities"""
        return self.amenity_repo.get_all()
    
    def get_amenity_by_name(self, name):
        """Get amenity by name"""
        return self.amenity_repo.get_by_attribute('name', name)
    
    def update_amenity(self, amenity_id, amenity_data):
        """Update amenity information"""
        amenity = self.amenity_repo.get(amenity_id)
        if amenity:
            amenity.update(amenity_data)
            return self.amenity_repo.update(amenity_id, amenity)
        return None
    
    def delete_amenity(self, amenity_id):
        """Delete an amenity"""
        return self.amenity_repo.delete(amenity_id)

# Global facade instance
facade = HBnBFacade()
