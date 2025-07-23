from flask_restx import Namespace, Resource, fields
from flask import request
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=False, description="List of amenities ID's")
})

# Define response models
place_response_model = api.model('PlaceResponse', {
    'id': fields.String(required=True, description='Place ID'),
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner')
})

place_list_model = api.model('PlaceListItem', {
    'id': fields.String(required=True, description='Place ID'),
    'title': fields.String(required=True, description='Title of the place'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place')
})

place_detail_model = api.model('PlaceDetail', {
    'id': fields.String(required=True, description='Place ID'),
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner': fields.Nested(user_model, description='Owner details'),
    'amenities': fields.List(fields.Nested(amenity_model), description='List of amenities')
})

review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

place_full_model = api.model('PlaceFull', { 
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'owner': fields.Nested(user_model, description='Owner of the place'),
    'amenities': fields.List(fields.Nested(amenity_model), description='List of amenities'),
    'reviews': fields.List(fields.Nested(review_model), description='List of reviews')
    })

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created', place_response_model)
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new place"""
        try:
            # Get data from request
            place_data = request.get_json()
            
            # Create place using facade
            current_user = get_jwt_identity()
            place_data['owner_id'] = current_user['id']  # Sécuriser l'attribution
            place = facade.create_place(place_data)
                        
            # Return place details
            return {
                'id': place.id,
                'title': place.title,
                'description': place.description,
                'price': place.price,
                'latitude': place.latitude,
                'longitude': place.longitude,
                'owner_id': place.owner_id
            }, 201
            
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'An error occurred while creating the place'}, 400

    @api.response(200, 'List of places retrieved successfully', [place_list_model])
    def get(self):
        """Retrieve a list of all places"""
        try:
            # Get all places using facade
            places = facade.get_all_places()
            
            # Format response - only basic info for list view
            place_list = []
            for place in places:
                place_list.append({
                    'id': place.id,
                    'title': place.title,
                    'latitude': place.latitude,
                    'longitude': place.longitude
                })
            
            return place_list, 200
            
        except Exception as e:
            return {'error': 'An error occurred while retrieving places'}, 500

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully', place_detail_model)
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        try:
            # Get place using facade
            place = facade.get_place(place_id)
            
            if not place:
                return {'error': 'Place not found'}, 404
            
            # Get owner details
            owner = facade.get_user_by_id(place.owner_id)
            owner_data = None
            if owner:
                owner_data = {
                    'id': owner.id,
                    'first_name': owner.first_name,
                    'last_name': owner.last_name,
                    'email': owner.email
                }
            
            # Get amenities details
            amenities_data = []
            if place.amenities:
                amenities = facade.get_amenities_by_ids(place.amenities)
                for amenity in amenities:
                    amenities_data.append({
                        'id': amenity.id,
                        'name': amenity.name
                    })
            
            # Return detailed place info with relationships
            return {
                'id': place.id,
                'title': place.title,
                'description': place.description,
                'latitude': place.latitude,
                'longitude': place.longitude,
                'owner': owner_data,
                'amenities': amenities_data
            }, 200
            
        except Exception as e:
            return {'error': 'An error occurred while retrieving the place'}, 500

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, place_id):
        """Update a place's information"""
        current_user = get_jwt_identity()
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        
        """Update a place's information (owner or admin only)"""
        is_admin = current_user.get('is_admin', False)
        if not is_admin and place.owner_id != current_user['id']:
            return {'error': 'Unauthorized action'}, 403
        
        try:
            # Get data from request
            place_data = request.get_json()
            
            # Update place using facade
            updated_place = facade.update_place(place_id, place_data)
            
            if not updated_place:
                return {'error': 'Place not found'}, 404
            
            # Return success message
            return {'message': 'Place updated successfully'}, 200
            
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'An error occurred while updating the place'}, 400