from app.models.place import Place
from app.models.amenity import Amenity
from app import db
from app.persistence.repository import SQLAlchemyRepository

class PlaceRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Place)

    def get_by_price_range(self, min_price, max_price):
        return self.model.query.filter(Place.price >= min_price, Place.price <= max_price).all()
    
    def get_by_owner(self, owner_id):
        return self.model.query.filter(Place.owner_id == owner_id).all()
    
    def get_places_by_ids(self, place_ids):
        """Retrieve places by their IDs."""
        # Assuming place_ids is a list of integers (IDs of the places)
        return self.model.query.filter(Place.id.in_(place_ids)).all()