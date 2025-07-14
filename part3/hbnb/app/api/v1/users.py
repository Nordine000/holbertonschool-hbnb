from flask_restx import Namespace, Resource, fields
from app.services import facade
from models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity




api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload
        password = user_data.pop('password')  # Retire le mot de passe en clair
        user = User(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            email=user_data['email']
        )
        user.hash_password(password)


        # Simulate email uniqueness check (to be replaced by real validation with persistence)
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        new_user = facade.user_repository.add(user)
        return {'id': new_user.id, 'first_name': new_user.first_name, 'last_name': new_user.last_name, 'email': new_user.email }, 201
    
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def get(self):
        users = facade.get_all_users()
        return [{"id": user.id, "first_name": user.first_name, "last_name": user.last_name, "email": user.email}
                for user in users
                ], 200
    


@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    @jwt_required()
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}, 200
    
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, user_id):
        update_data = api.payload
        current_user = get_jwt_identity()
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        
        if user_id != current_user['id']:
            return {'error': 'Action non autorisée'}, 403

        if 'email' in api.payload or 'password' in api.payload:
            return {'error': 'Vous ne pouvez pas modifier votre adresse e-mail ou votre mot de passe'}, 400
        
        updated_user = facade.update_user(user_id, update_data)
        return {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}, 200
    

