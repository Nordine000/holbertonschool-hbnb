from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'place_id': fields.String(required=True, description='ID of the place')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new review"""
        current_user = get_jwt_identity()
        review_data = api.payload
        place = facade.get_place(review_data['place_id'])

        if not place:
            return {"error": "Place not found"}, 404

        if place.owner_id == current_user['id']:
            return {"error": "Vous ne pouvez pas évaluer votre propre lieu"}, 400

        existing_review = facade.get_review_by_user_and_place(current_user['id'], review_data['place_id'])
        if existing_review:
            return {"error": "Vous avez déjà évalué ce lieu"}, 400

        review_data['user_id'] = current_user['id']

        try:
            review = facade.create_review(review_data)
            return {
                "id": review.id,
                "text": review.text,
                "rating": review.rating,
                "user_id": review.user_id,
                "place_id": review.place_id,
                "created_at": review.created_at.isoformat()
            }, 201
        except ValueError as e:
            return {"error": str(e)}, 400
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}, 400


    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        try:
            reviews = facade.get_all_reviews()
            return [{
                "id": r.id,
                "text": r.text,
                "rating": r.rating,
                "created_at": r.created_at.isoformat()
            } for r in reviews], 200

        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}, 500


@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404

        return {
            "id": review.id,
            "text": review.text,
            "rating": review.rating,
            "user_id": review.user_id,
            "place_id": review.place_id,
            "created_at": review.created_at.isoformat(),
            "updated_at": review.updated_at.isoformat()
        }, 200

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, review_id):
        """Update a review's information"""
        current_user = get_jwt_identity()
        review = facade.get_review(review_id)

        if not review:
            return {"error": "Review not found"}, 404

        is_admin = current_user.get('is_admin', False)
        if not is_admin and review.user_id != current_user['id']:
            return {"error": "Action non autorisée"}, 403
        
        try:
            review_data = api.payload
            updated = facade.update_review(review_id, review_data)

            if not updated:
                return {"error": "Review not found"}, 404

            return {"message": "Review updated successfully"}, 200

        except ValueError as e:
            return {"error": str(e)}, 400


    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""
        current_user = get_jwt_identity()
        review = facade.get_review(review_id)

        if not review:
            return {"error": "Review not found"}, 404

        is_admin = current_user.get('is_admin', False)
        if not is_admin and review.user_id != current_user['id']:
            return {"error": "Action non autorisée"}, 403

        
        deleted = facade.delete_review(review_id)
        if not deleted:
            return {"error": "Review not found"}, 404

        return {"message": "Review deleted successfully"}, 200

@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        try:
            reviews = facade.get_reviews_by_place(place_id)

            if not reviews:
                return {"error": "Place not found or has no reviews"}, 404

            return [{
                "id": r.id,
                "text": r.text,
                "rating": r.rating,
                "created_at": r.created_at.isoformat()
            } for r in reviews], 200

        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}, 500