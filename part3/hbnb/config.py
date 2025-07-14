import os
from datetime import timedelta

class Config:
    """Base configuration class"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # JWT Configuration - uses Flask's SECRET_KEY for signing tokens
    JWT_SECRET_KEY = SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_ALGORITHM = 'HS256'
    
class DevelopmentConfig(Config):
    """Configuration for development environment"""
    DEBUG = True
    
class ProductionConfig(Config):
    """Configuration for production environment"""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY must be set in production")
    
class TestingConfig(Config):
    """Configuration for testing environment"""
    TESTING = True
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=1)  # Short expiry for tests
