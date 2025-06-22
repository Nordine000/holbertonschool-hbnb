from flask_restx import Namespace, Resource, fields
from flask import request
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

# Define the response model
amenity_response_model = api.model('AmenityResponse', {
    'id': fields.String(required=True, description='Unique identifier of the amenity'),
    'name': fields.String(required=True, description='Name of the amenity')
})

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created', amenity_response_model)
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        try:
            # Get data from request
            amenity_data = request.get_json()
            
            # Create amenity using facade
            amenity = facade.create_amenity(amenity_data)
            
            # Return amenity details
            return {
                'id': amenity.id,
                'name': amenity.name
            }, 201
            
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'An error occurred while creating the amenity'}, 400

    @api.response(200, 'List of amenities retrieved successfully', [amenity_response_model])
    def get(self):
        """Retrieve a list of all amenities"""
        try:
            # Get all amenities using facade
            amenities = facade.get_all_amenities()
            
            # Format response
            amenity_list = []
            for amenity in amenities:
                amenity_list.append({
                    'id': amenity.id,
                    'name': amenity.name
                })
            
            return amenity_list, 200
            
        except Exception as e:
            return {'error': 'An error occurred while retrieving amenities'}, 500

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully', amenity_response_model)
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        try:
            # Get amenity using facade
            amenity = facade.get_amenity(amenity_id)
            
            if not amenity:
                return {'error': 'Amenity not found'}, 404
            
            # Return amenity details
            return {
                'id': amenity.id,
                'name': amenity.name
            }, 200
            
        except Exception as e:
            return {'error': 'An error occurred while retrieving the amenity'}, 500

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        try:
            # Get data from request
            amenity_data = request.get_json()
            
            # Update amenity using facade
            updated_amenity = facade.update_amenity(amenity_id, amenity_data)
            
            if not updated_amenity:
                return {'error': 'Amenity not found'}, 404
            
            # Return success message
            return {'message': 'Amenity updated successfully'}, 200
            
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'An error occurred while updating the amenity'}, 400