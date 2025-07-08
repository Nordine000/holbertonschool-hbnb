#!/usr/bin/python3
"""
Authentication API endpoints for JWT-based login
"""
from flask import Blueprint, request, jsonify
from flask_restx import Namespace, Resource, fields, Api
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.services.facade import facade

# Create Blueprint
auth_bp = Blueprint('auth', __name__)
api = Api(auth_bp, doc='/doc/', title='Authentication API', version='1.0')

# Create namespace
auth_ns = api.namespace('auth', description='Authentication operations')

# Model for input validation
login_model = auth_ns.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model)
    @auth_ns.doc('user_login')
    def post(self):
        """Authenticate user and return a JWT token"""
        try:
            credentials = auth_ns.payload  # Get the email and password from the request payload
            
            if not credentials:
                return {'error': 'No credentials provided'}, 400
            
            # Step 1: Retrieve the user based on the provided email
            user = facade.get_user_by_email(credentials['email'])
            
            # Step 2: Check if the user exists and the password is correct
            if not user or not user.verify_password(credentials['password']):
                return {'error': 'Invalid credentials'}, 401

            # Step 3: Create a JWT token with the user's id and is_admin flag
            access_token = create_access_token(
                identity={'id': str(user.id), 'is_admin': user.is_admin}
            )
            
            # Step 4: Return the JWT token to the client
            return {'access_token': access_token}, 200
            
        except Exception as e:
            return {'error': str(e)}, 500

@auth_ns.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    @auth_ns.doc('protected_endpoint')
    def get(self):
        """A protected endpoint that requires a valid JWT token"""
        try:
            current_user = get_jwt_identity()  # Retrieve the user's identity from the token
            return {
                'message': f'Hello, user {current_user["id"]}',
                'user_id': current_user['id'],
                'is_admin': current_user['is_admin']
            }, 200
        except Exception as e:
            return {'error': str(e)}, 500

# Alternative Blueprint-based approach (without flask-restx)
auth_bp_simple = Blueprint('auth_simple', __name__)

@auth_bp_simple.route('/login', methods=['POST'])
def login():
    """Simple login endpoint without flask-restx"""
    try:
        data = request.get_json()
        
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password are required'}), 400
        
        # Step 1: Retrieve the user based on the provided email
        user = facade.get_user_by_email(data['email'])
        
        # Step 2: Check if the user exists and the password is correct
        if not user or not user.verify_password(data['password']):
            return jsonify({'error': 'Invalid credentials'}), 401

        # Step 3: Create a JWT token with the user's id and is_admin flag
        access_token = create_access_token(
            identity={'id': str(user.id), 'is_admin': user.is_admin}
        )
        
        # Step 4: Return the JWT token to the client
        return jsonify({'access_token': access_token}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp_simple.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    """A protected endpoint that requires a valid JWT token"""
    try:
        current_user = get_jwt_identity()  # Retrieve the user's identity from the token
        return jsonify({
            'message': f'Hello, user {current_user["id"]}',
            'user_id': current_user['id'],
            'is_admin': current_user['is_admin']
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
