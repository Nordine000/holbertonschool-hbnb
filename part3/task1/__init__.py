from flask import Flask
from flask_bcrypt import Bcrypt

# Initialize bcrypt instance
bcrypt = Bcrypt()

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
    
    # Initialize bcrypt with the app
    bcrypt.init_app(app)
    
    # Here you can add other extension initialization
    # and blueprint registration in future tasks
    
    return app
