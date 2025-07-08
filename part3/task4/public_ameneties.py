#!/usr/bin/python3
"""
Amenities API endpoints (public access for reading)
"""
from flask import Blueprint, request, jsonify
from app.services.facade import facade

# Create blueprint for amenities
amenities_bp = Blueprint('amenities', __name__)

@amenities_bp.route('/', methods=['GET'])
def get_all_amenities():
    """
    Get all amenities (public endpoint)
    """
    try:
        amenities = facade.get_all_amenities()
        return jsonify([amenity.to_dict() for amenity in amenities]), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@amenities_bp.route('/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    """
    Get a specific amenity by ID (public endpoint)
    """
    try:
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return jsonify({'error': 'Amenity not found'}), 404
        
        return jsonify(amenity.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
