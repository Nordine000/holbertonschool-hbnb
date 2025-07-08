#!/usr/bin/python3
"""
Reviews API endpoints with JWT authentication
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import facade

# Create blueprint for reviews
reviews_bp = Blueprint('reviews', __name__)

@reviews_bp.route('/', methods=['POST'])
@jwt_required()
def create_review():
    """
    Create a new review (authenticated users only)
    Users cannot review their own places or review a place multiple times
    """
    try:
        current_user = get_jwt_identity()
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['text', 'rating', 'place_id']
        if not data or not all(field in data for field in required_fields):
            return jsonify({
                'error': 'Missing required fields: text, rating, place_id'
            }), 400
        
        # Validate rating range
        try:
            rating = int(data['rating'])
            if rating < 1 or rating > 5:
                return jsonify({'error': 'Rating must be between 1 and 5'}), 400
        except (ValueError, TypeError):
            return jsonify({'error': 'Rating must be an integer between 1 and 5'}), 400
        
        # Check if the place exists
        place = facade.get_place(data['place_id'])
        if not place:
            return jsonify({'error': 'Place not found'}), 404
        
        # Check if user is trying to review their own place
        if place.owner_id == current_user['id']:
            return jsonify({'error': 'You cannot review your own place'}), 400
        
        # Check if user has already reviewed this place
        existing_review = facade.get_user_review_for_place(current_user['id'], data['place_id'])
        if existing_review:
            return jsonify({'error': 'You have already reviewed this place'}), 400
        
        # Set the user_id to the authenticated user
        data['user_id'] = current_user['id']
        
        # Create new review
        new_review = facade.create_review(data)
        
        return jsonify({
            'id': new_review.id,
            'message': 'Review created successfully'
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@reviews_bp.route('/', methods=['GET'])
def get_all_reviews():
    """
    Get all reviews (public endpoint)
    """
    try:
        reviews = facade.get_all_reviews()
        return jsonify([review.to_dict() for review in reviews]), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@reviews_bp.route('/<review_id>', methods=['GET'])
def get_review(review_id):
    """
    Get a specific review by ID (public endpoint)
    """
    try:
        review = facade.get_review(review_id)
        if not review:
            return jsonify({'error': 'Review not found'}), 404
        
        return jsonify(review.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@reviews_bp.route('/<review_id>', methods=['PUT'])
@jwt_required()
def update_review(review_id):
    """
    Update a review (only the author can modify)
    """
    try:
        current_user = get_jwt_identity()
        review = facade.get_review(review_id)
        
        if not review:
            return jsonify({'error': 'Review not found'}), 404
        
        # Check if the current user is the author of the review
        if review.user_id != current_user['id']:
            return jsonify({'error': 'Unauthorized action'}), 403
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate rating if provided
        if 'rating' in data:
            try:
                rating = int(data['rating'])
                if rating < 1 or rating > 5:
                    return jsonify({'error': 'Rating must be between 1 and 5'}), 400
            except (ValueError, TypeError):
                return jsonify({'error': 'Rating must be an integer between 1 and 5'}), 400
        
        # Update review
        updated_review = facade.update_review(review_id, data)
        return jsonify(updated_review.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@reviews_bp.route('/<review_id>', methods=['DELETE'])
@jwt_required()
def delete_review(review_id):
    """
    Delete a review (only the author can delete)
    """
    try:
        current_user = get_jwt_identity()
        review = facade.get_review(review_id)
        
        if not review:
            return jsonify({'error': 'Review not found'}), 404
        
        # Check if the current user is the author of the review
        if review.user_id != current_user['id']:
            return jsonify({'error': 'Unauthorized action'}), 403
        
        facade.delete_review(review_id)
        return jsonify({'message': 'Review deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@reviews_bp.route('/places/<place_id>', methods=['GET'])
def get_reviews_by_place(place_id):
    """
    Get all reviews for a specific place (public endpoint)
    """
    try:
        # Check if place exists
        place = facade.get_place(place_id)
        if not place:
            return jsonify({'error': 'Place not found'}), 404
        
        reviews = facade.get_reviews_by_place(place_id)
        return jsonify([review.to_dict() for review in reviews]), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
