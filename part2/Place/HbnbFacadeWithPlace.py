# services/facade.py
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.user import User  # Assuming User model exists
from app.persistence.repository import InMemoryRepository

class HBnBFacade:
    def __init__(self):
        self.amenity_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.user_repo = InMemoryRepository()  # Assuming users are stored here
    
    # Amenity methods (from previous task)
    def create_amenity(self, amenity_data):
        """Create a new amenity"""
        if not amenity_data.get('name'):
            raise ValueError("Amenity name is required")
        
        existing_amenities = self.amenity_repo.get_all()
        for amenity in existing_amenities:
            if amenity.name.lower() == amenity_data['name'].lower():
                raise ValueError("Amenity with this name already exists")
        
        amenity = Amenity(name=amenity_data['name'])
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Retrieve an amenity by ID"""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """Retrieve all amenities"""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Update an amenity"""
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        
        if 'name' in amenity_data:
            if not amenity_data['name']:
                raise ValueError("Amenity name cannot be empty")
            
            existing_amenities = self.amenity_repo.get_all()
            for existing_amenity in existing_amenities:
                if (existing_amenity.id != amenity_id and 
                    existing_amenity.name.lower() == amenity_data['name'].lower()):
                    raise ValueError("Amenity with this name already exists")
            
            amenity.name = amenity_data['name']
        
        self.amenity_repo.update(amenity_id, amenity)
        return amenity
    
    # Place methods
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
            place = Place(
                title=place_data['title'],
                description=place_data.get('description', ''),
                price=place_data['price'],
                latitude=place_data['latitude'],
                longitude=place_data['longitude'],
                owner_id=place_data['owner_id'],
                amenities=amenities
            )
            self.place_repo.add(place)
            return place
        except ValueError as e:
            raise ValueError(f"Invalid place data: {str(e)}")

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
