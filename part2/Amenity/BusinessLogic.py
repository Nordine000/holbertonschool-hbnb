# services/facade.py
from app.models.amenity import Amenity
from app.persistence.repository import InMemoryRepository

class HBnBFacade:
    def __init__(self):
        self.amenity_repo = InMemoryRepository()
    
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
        # Get existing amenity
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        
        # Validate new name if provided
        if 'name' in amenity_data:
            if not amenity_data['name']:
                raise ValueError("Amenity name cannot be empty")
            
            # Check if another amenity with same name already exists
            existing_amenities = self.amenity_repo.get_all()
            for existing_amenity in existing_amenities:
                if (existing_amenity.id != amenity_id and 
                    existing_amenity.name.lower() == amenity_data['name'].lower()):
                    raise ValueError("Amenity with this name already exists")
            
            amenity.name = amenity_data['name']
        
        self.amenity_repo.update(amenity_id, amenity)
        return amenity
