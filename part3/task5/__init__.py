from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

# Initialize extensions
bcrypt = Bcrypt()
jwt = JWTManager()
db = SQLAlchemy()

def create_app(config_class="config.DevelopmentConfig"):
    """
    Application Factory to create Flask application with configuration
    
    Args:
        config_class (str): Configuration class to use
                           Default: "config.DevelopmentConfig"
    
    Returns:
        Flask: Configured Flask application instance
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions with the app
    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)
    
    # Configure JWT error handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return {'error': 'Token has expired'}, 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return {'error': 'Invalid token'}, 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return {'error': 'Authorization token is required'}, 401
    
    # Register blueprints (will be added when models are mapped)
    # from api.v1.auth import auth_bp
    # from api.v1.users import users_bp
    # from api.v1.places import places_bp
    # from api.v1.reviews import reviews_bp
    # from api.v1.amenities import amenities_bp
    # from api.v1.admin import admin_bp
    
    # app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    # app.register_blueprint(users_bp, url_prefix='/api/v1/users')
    # app.register_blueprint(places_bp, url_prefix='/api/v1/places')
    # app.register_blueprint(reviews_bp, url_prefix='/api/v1/reviews')
    # app.register_blueprint(amenities_bp, url_prefix='/api/v1/amenities')
    # app.register_blueprint(admin_bp, url_prefix='/api/v1/admin')
    
    return app
