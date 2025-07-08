#!/usr/bin/python3
"""
Users API endpoints with JWT protection
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import facade

# Create blueprint for users
users_bp = Blueprint('users', __name__)

@users_bp.route('/', methods=['POST'])
def create_user():
    """
    Create a new user (public endpoint - no JWT required for registration)
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['first_name', 'last_name', 'email', 'password']
        if not data or not all(field in data for field in required_fields):
            return jsonify({
                'error': 'Missing required fields: first_name, last_name, email, password'
            }), 400
        
        # Check if email already exists
        existing_user = facade.get_user_by_email(data['email'])
        if existing_user:
            return jsonify({'error': 'Email already registered'}), 400
        
        # Create new user
        new_user = facade.create_user(data)
        
        # Return success response without password
        return jsonify({
            'id': new_user.id,
            'message': 'User created successfully'
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_users():
    """
    Get all users (protected endpoint - requires JWT)
    """
    try:
        current_user = get_jwt_identity()
        
        # Only admins can view all users
        if not current_user.get('is_admin', False):
            return jsonify({'error': 'Admin access required'}), 403
        
        users = facade.get_all_users()
        return jsonify([user.to_dict() for user in users]), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/<user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    """
    Get a specific user by ID (protected endpoint)
    Users can only view their own profile unless they are admin
    """
    try:
        current_user = get_jwt_identity()
        
        # Check if user is trying to access their own profile or is admin
        if current_user['id'] != user_id and not current_user.get('is_admin', False):
            return jsonify({'error': 'Access denied'}), 403
        
        user = facade.get_user(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify(user.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/<user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    """
    Update a user's information (protected endpoint)
    Users can only update their own profile unless they are admin
    """
    try:
        current_user = get_jwt_identity()
        
        # Check if user is trying to update their own profile or is admin
        if current_user['id'] != user_id and not current_user.get('is_admin', False):
            return jsonify({'error': 'Access denied'}), 403
        
        user = facade.get_user(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Prevent non-admins from changing admin status
        if 'is_admin' in data and not current_user.get('is_admin', False):
            return jsonify({'error': 'Cannot modify admin status'}), 403
        
        updated_user = facade.update_user(user_id, data)
        return jsonify(updated_user.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/<user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    """
    Delete a user (admin only)
    """
    try:
        current_user = get_jwt_identity()
        
        # Only admins can delete users
        if not current_user.get('is_admin', False):
            return jsonify({'error': 'Admin access required'}), 403
        
        user = facade.get_user(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        facade.delete_user(user_id)
        return jsonify({'message': 'User deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """
    Get current user's profile
    """
    try:
        current_user = get_jwt_identity()
        user = facade.get_user(current_user['id'])
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify(user.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
