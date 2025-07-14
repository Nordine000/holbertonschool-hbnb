from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user
    
    def get_user(self, user_id):
        return self.user_repo.get(user_id)
    
    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)
    
    def get_all_users(self):
        return self.user_repo.get_all()
    
    def update_user(self, user_id, update_data):
        user = self.get_user(user_id)
        if not user:
            return None
        for key, value in update_data.items():
            setattr(user, key, value)
        self.user_repo.update(user_id, user)
        return user
    
    def create_amenity(self, amenity_data):
        """Create a new amenity"""
        # Validate that name is provided
        if not amenity_data.get('name'):
            raise ValueError("Amenity name is required")
        
        # Check if amenity with same name already exists
        existing_amenities = self.amenity_repo.get_all()
        for amenity in existing_amenities:
            if amenity.name.lower() == amenity_data['name'].lower():
                raise ValueError("Amenity with this name already exists")
        
        # Create new amenity
        amenity = Amenity(name=amenity_data['name'])
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Retrieve an amenity by ID"""
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        return amenity

    def get_all_amenities(self):
        """Retrieve all amenities"""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Update an amenity"""
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None

        if 'name' in amenity_data:
            new_name = amenity_data['name']
            if not new_name:
                raise ValueError("Amenity name cannot be empty")
            # Vérifie les doublons
            existing_amenities = self.amenity_repo.get_all()
            for existing_amenity in existing_amenities:
                if (existing_amenity.id != amenity_id and 
                    existing_amenity.name.lower() == new_name.lower()):
                    raise ValueError("Amenity with this name already exists")

            try:
                amenity.name = new_name
            except Exception as e:
                raise ValueError(f"Invalid name: {str(e)}")

        self.amenity_repo.update(amenity_id, amenity_data)
        return amenity

    def create_place(self, place_data):
        """Create a new place with validation for price, latitude, and longitude"""
        # Validate required fields
        required_fields = ['title', 'price', 'latitude', 'longitude', 'owner_id']
        for field in required_fields:
            if field not in place_data:
                raise ValueError(f"{field} is required")
        
        # Verify that the owner exists
        owner = self.user_repo.get(place_data['owner_id'])
        if not owner:
            raise ValueError("Owner not found")
        
        # Verify that all amenities exist
        amenities = place_data.get('amenities', [])
        for amenity_id in amenities:
            amenity = self.amenity_repo.get(amenity_id)
            if not amenity:
                raise ValueError(f"Amenity with ID {amenity_id} not found")
        
        # Create place (validation happens in the constructor via setters)
        try:
            print(f"[DEBUG] owner: {owner}, type: {type(owner)}")

            place = Place(
            title=place_data['title'],
            description=place_data.get('description', ''),
            price=place_data['price'],
            latitude=place_data['latitude'],
            longitude=place_data['longitude'],
            owner=owner,
            )
            for amenity_id in place_data.get('amenities', []):
                place.add_amenity(amenity_id)

            self.place_repo.add(place)
            return place
        except Exception as e:
            print(f"[Erreur] Exception levée : {e}")
            return {"error": str(e)}
        except Exception as e:
            print(f"[Erreur] Exception levée : {e}")
            raise


    def get_place(self, place_id):
        """Retrieve a place by ID, including associated owner and amenities"""
        place = self.place_repo.get(place_id)
        if not place:
            return None
        return place

    def get_all_places(self):
        """Retrieve all places"""
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """Update a place"""
        place = self.place_repo.get(place_id)
        if not place:
            return None
        
        # Verify owner exists if owner_id is being updated
        if 'owner_id' in place_data:
            owner = self.user_repo.get(place_data['owner_id'])
            if not owner:
                raise ValueError("Owner not found")
        
        # Verify amenities exist if amenities are being updated
        if 'amenities' in place_data:
            for amenity_id in place_data['amenities']:
                amenity = self.amenity_repo.get(amenity_id)
                if not amenity:
                    raise ValueError(f"Amenity with ID {amenity_id} not found")
        
        # Update place (validation happens via setters)
        try:
            place.update(place_data)
            self.place_repo.update(place_id, place)
            return place
        except ValueError as e:
            raise ValueError(f"Invalid update data: {str(e)}")
    
    # Helper methods to get related data
    def get_user_by_id(self, user_id):
        """Get user details by ID"""
        return self.user_repo.get(user_id)
    
    def get_amenities_by_ids(self, amenity_ids):
        """Get amenities details by their IDs"""
        amenities = []
        for amenity_id in amenity_ids:
            amenity = self.amenity_repo.get(amenity_id)
            if amenity:
                amenities.append(amenity)
        return amenities
    
    def create_review(self, review_data):
        required_fields = ['user_id', 'place_id', 'rating', 'comment']
        for field in required_fields:
            if field not in review_data:
                raise ValueError(f"{field} is required")

        user = self.user_repo.get(review_data['user_id'])
        if not user:
            raise ValueError("User not found")

        place = self.place_repo.get(review_data['place_id'])
        if not place:
            raise ValueError("Place not found")

        review = Review(
            user=user,
            place=place,
            rating=review_data['rating'],
            text=review_data['comment']
            )
        self.review_repo.add(review)
        return review
    
    def get_review(self, review_id):
        return self.review_repo.get(review_id)
    
    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        return [r for r in self.review_repo.get_all() if r.place_id == place_id]

    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)
        if not review:
            return None

        if 'rating' in review_data:
            review.rating = review_data['rating']
        if 'comment' in review_data:
            review.comment = review_data['comment']

        self.review_repo.update(review_id, {
            "rating": review.rating,
            "comment": review.comment
        })
        return review

    def delete_review(self, review_id):
        return self.review_repo.delete(review_id)
