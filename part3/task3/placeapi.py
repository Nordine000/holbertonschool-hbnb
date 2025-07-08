#!/usr/bin/python3
"""
Places API endpoints with JWT authentication
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import facade

# Create blueprint for places
places_bp = Blueprint('places', __name__)

@places_bp.route('/', methods=['POST'])
@jwt_required()
def create_place():
    """
    Create a new place (authenticated users only)
    """
    try:
        current_user = get_jwt_identity()
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['title', 'description', 'price', 'latitude', 'longitude']
        if not data or not all(field in data for field in required_fields):
            return jsonify({
                'error': 'Missing required fields: title, description, price, latitude, longitude'
            }), 400
        
        # Set the owner_id to the authenticated user
        data['owner_id'] = current_user['id']
        
        # Validate data types
        try:
            data['price'] = float(data['price'])
            data['latitude'] = float(data['latitude'])
            data['longitude'] = float(data['longitude'])
        except (ValueError, TypeError):
            return jsonify({'error': 'Price, latitude, and longitude must be numbers'}), 400
        
        # Create new place
        new_place = facade.create_place(data)
        
        return jsonify({
            'id': new_place.id,
            'message': 'Place created successfully'
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@places_bp.route('/', methods=['GET'])
def get_all_places():
    """
    Get all places (public endpoint - no authentication required)
    """
    try:
        places = facade.get_all_places()
        return jsonify([place.to_dict() for place in places]), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@places_bp.route('/<place_id>', methods=['GET'])
def get_place(place_id):
    """
    Get a specific place by ID (public endpoint - no authentication required)
    """
    try:
        place = facade.get_place(place_id)
        if not place:
            return jsonify({'error': 'Place not found'}), 404
        
        return jsonify(place.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@places_bp.route('/<place_id>', methods=['PUT'])
@jwt_required()
def update_place(place_id):
    """
    Update a place's details (only the owner can modify)
    """
    try:
        current_user = get_jwt_identity()
        place = facade.get_place(place_id)
        
        if not place:
            return jsonify({'error': 'Place not found'}), 404
        
        # Check if the current user is the owner of the place
        if place.owner_id != current_user['id']:
            return jsonify({'error': 'Unauthorized action'}), 403
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate numeric fields if provided
        if 'price' in data:
            try:
                data['price'] = float(data['price'])
            except (ValueError, TypeError):
                return jsonify({'error': 'Price must be a number'}), 400
        
        if 'latitude' in data:
            try:
                data['latitude'] = float(data['latitude'])
            except (ValueError, TypeError):
                return jsonify({'error': 'Latitude must be a number'}), 400
        
        if 'longitude' in data:
            try:
                data['longitude'] = float(data['longitude'])
            except (ValueError, TypeError):
                return jsonify({'error': 'Longitude must be a number'}), 400
        
        # Update place
        updated_place = facade.update_place(place_id, data)
        return jsonify(updated_place.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@places_bp.route('/<place_id>', methods=['DELETE'])
@jwt_required()
def delete_place(place_id):
    """
    Delete a place (only the owner can delete)
    """
    try:
        current_user = get_jwt_identity()
        place = facade.get_place(place_id)
        
        if not place:
            return jsonify({'error': 'Place not found'}), 404
        
        # Check if the current user is the owner of the place
        if place.owner_id != current_user['id']:
            return jsonify({'error': 'Unauthorized action'}), 403
        
        facade.delete_place(place_id)
        return jsonify({'message': 'Place deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
