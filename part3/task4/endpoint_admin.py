#!/usr/bin/python3
"""
Admin API endpoints for administrative operations
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import facade

# Create blueprint for admin operations
admin_bp = Blueprint('admin', __name__)

def require_admin():
    """Helper function to check admin privileges"""
    current_user = get_jwt_identity()
    if not current_user.get('is_admin', False):
        return {'error': 'Admin privileges required'}, 403
    return None

# USER MANAGEMENT ENDPOINTS

@admin_bp.route('/users/', methods=['POST'])
@jwt_required()
def admin_create_user():
    """
    Create a new user (admin only)
    """
    try:
        # Check admin privileges
        admin_check = require_admin()
        if admin_check:
            return jsonify(admin_check[0]), admin_check[1]
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['first_name', 'last_name', 'email']
        if not data or not all(field in data for field in required_fields):
            return jsonify({
                'error': 'Missing required fields: first_name, last_name, email'
            }), 400
        
        # Check if email already exists
        existing_user = facade.get_user_by_email(data['email'])
        if existing_user:
            return jsonify({'error': 'Email already registered'}), 400
        
        # Set default password if not provided
        if 'password' not in data:
            data['password'] = 'default_password123'
        
        # Create new user
        new_user = facade.create_user(data)
        
        return jsonify({
            'id': new_user.id,
            'message': 'User created successfully'
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/users/<user_id>', methods=['PUT'])
@jwt_required()
def admin_modify_user(user_id):
    """
    Modify any user's details (admin only)
    Can modify email and password
    """
    try:
        # Check admin privileges
        admin_check = require_admin()
        if admin_check:
            return jsonify(admin_check[0]), admin_check[1]
        
        user = facade.get_user(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Check email uniqueness if email is being updated
        if 'email' in data:
            existing_user = facade.get_user_by_email(data['email'])
            if existing_user and existing_user.id != user_id:
                return jsonify({'error': 'Email already in use'}), 400
        
        # Update user
        updated_user = facade.update_user(user_id, data)
        return jsonify(updated_user.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/users/<user_id>', methods=['DELETE'])
@jwt_required()
def admin_delete_user(user_id):
    """
    Delete any user (admin only)
    """
    try:
        # Check admin privileges
        admin_check = require_admin()
        if admin_check:
            return jsonify(admin_check[0]), admin_check[1]
        
        user = facade.get_user(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        facade.delete_user(user_id)
        return jsonify({'message': 'User deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# AMENITY MANAGEMENT ENDPOINTS

@admin_bp.route('/amenities/', methods=['POST'])
@jwt_required()
def admin_create_amenity():
    """
    Add a new amenity (admin only)
    """
    try:
        # Check admin privileges
        admin_check = require_admin()
        if admin_check:
            return jsonify(admin_check[0]), admin_check[1]
        
        data = request.get_json()
        
        # Validate required fields
        if not data or 'name' not in data:
            return jsonify({'error': 'Missing required field: name'}), 400
        
        # Check if amenity name already exists
        existing_amenity = facade.get_amenity_by_name(data['name'])
        if existing_amenity:
            return jsonify({'error': 'Amenity with this name already exists'}), 400
        
        # Create new amenity
        new_amenity = facade.create_amenity(data)
        
        return jsonify({
            'id': new_amenity.id,
            'message': 'Amenity created successfully'
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/amenities/<amenity_id>', methods=['PUT'])
@jwt_required()
def admin_modify_amenity(amenity_id):
    """
    Modify an amenity's details (admin only)
    """
    try:
        # Check admin privileges
        admin_check = require_admin()
        if admin_check:
            return jsonify(admin_check[0]), admin_check[1]
        
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return jsonify({'error': 'Amenity not found'}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Check name uniqueness if name is being updated
        if 'name' in data:
            existing_amenity = facade.get_amenity_by_name(data['name'])
            if existing_amenity and existing_amenity.id != amenity_id:
                return jsonify({'error': 'Amenity with this name already exists'}), 400
        
        # Update amenity
        updated_amenity = facade.update_amenity(amenity_id, data)
        return jsonify(updated_amenity.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/amenities/<amenity_id>', methods=['DELETE'])
@jwt_required()
def admin_delete_amenity(amenity_id):
    """
    Delete an amenity (admin only)
    """
    try:
        # Check admin privileges
        admin_check = require_admin()
        if admin_check:
            return jsonify(admin_check[0]), admin_check[1]
        
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return jsonify({'error': 'Amenity not found'}), 404
        
        facade.delete_amenity(amenity_id)
        return jsonify({'message': 'Amenity deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ADMIN OVERRIDE ENDPOINTS FOR PLACES AND REVIEWS

@admin_bp.route('/places/<place_id>', methods=['PUT'])
@jwt_required()
def admin_modify_place(place_id):
    """
    Modify any place (admin can bypass ownership restrictions)
    """
    try:
        current_user = get_jwt_identity()
        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')
        
        place = facade.get_place(place_id)
        if not place:
            return jsonify({'error': 'Place not found'}), 404
        
        # Check permissions: admin or owner
        if not is_admin and place.owner_id != user_id:
            return jsonify({'error': 'Unauthorized action'}), 403
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Update place
        updated_place = facade.update_place(place_id, data)
        return jsonify(updated_place.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/places/<place_id>', methods=['DELETE'])
@jwt_required()
def admin_delete_place(place_id):
    """
    Delete any place (admin can bypass ownership restrictions)
    """
    try:
        current_user = get_jwt_identity()
        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')
        
        place = facade.get_place(place_id)
        if not place:
            return jsonify({'error': 'Place not found'}), 404
        
        # Check permissions: admin or owner
        if not is_admin and place.owner_id != user_id:
            return jsonify({'error': 'Unauthorized action'}), 403
        
        facade.delete_place(place_id)
        return jsonify({'message': 'Place deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/reviews/<review_id>', methods=['PUT'])
@jwt_required()
def admin_modify_review(review_id):
    """
    Modify any review (admin can bypass ownership restrictions)
    """
    try:
        current_user = get_jwt_identity()
        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')
        
        review = facade.get_review(review_id)
        if not review:
            return jsonify({'error': 'Review not found'}), 404
        
        # Check permissions: admin or author
        if not is_admin and review.user_id != user_id:
            return jsonify({'error': 'Unauthorized action'}), 403
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Update review
        updated_review = facade.update_review(review_id, data)
        return jsonify(updated_review.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/reviews/<review_id>', methods=['DELETE'])
@jwt_required()
def admin_delete_review(review_id):
    """
    Delete any review (admin can bypass ownership restrictions)
    """
    try:
        current_user = get_jwt_identity()
        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')
        
        review = facade.get_review(review_id)
        if not review:
            return jsonify({'error': 'Review not found'}), 404
        
        # Check permissions: admin or author
        if not is_admin and review.user_id != user_id:
            return jsonify({'error': 'Unauthorized action'}), 403
        
        facade.delete_review(review_id)
        return jsonify({'message': 'Review deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
