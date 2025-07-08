#!/usr/bin/python3
"""
Users API endpoints for the HBnB application.
"""
from flask import Blueprint, request, jsonify
from models.user import User
from persistence.repository import InMemoryRepository

# Create blueprint for users
users_bp = Blueprint('users', __name__)

# Initialize repository (assuming you have this from previous tasks)
user_repo = InMemoryRepository()

@users_bp.route('/', methods=['POST'])
def create_user():
    """
    Create a new user with password hashing.
    
    Expected JSON:
    {
        "first_name": "John",
        "last_name": "Doe", 
        "email": "john@example.com",
        "password": "secretpassword"
    }
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
        existing_users = user_repo.get_all()
        for user in existing_users:
            if user.email == data['email']:
                return jsonify({'error': 'Email already registered'}), 400
        
        # Create new user (password will be automatically hashed in __init__)
        new_user = User(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            password=data['password']
        )
        
        # Save user to repository
        user_repo.add(new_user)
        
        # Return success response without password
        return jsonify({
            'id': new_user.id,
            'message': 'User created successfully'
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/', methods=['GET'])
def get_all_users():
    """
    Get all users (excluding passwords).
    """
    try:
        users = user_repo.get_all()
        return jsonify([user.to_dict() for user in users]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    """
    Get a specific user by ID (excluding password).
    
    Args:
        user_id (str): User's unique identifier
    """
    try:
        user = user_repo.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Return user data without password
        return jsonify(user.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/<user_id>', methods=['PUT'])
def update_user(user_id):
    """
    Update a user's information.
    
    Args:
        user_id (str): User's unique identifier
    """
    try:
        user = user_repo.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Update user (password will be hashed if provided)
        user.update(data)
        user_repo.update(user_id, user)
        
        # Return updated user data without password
        return jsonify(user.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Delete a user.
    
    Args:
        user_id (str): User's unique identifier
    """
    try:
        user = user_repo.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        user_repo.delete(user_id)
        return jsonify({'message': 'User deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
