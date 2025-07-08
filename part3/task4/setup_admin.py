#!/usr/bin/env python3
"""
Script to create an admin user for testing admin endpoints
"""
from app import create_app
from app.services.facade import facade

def create_admin_user():
    """Create an admin user for testing purposes"""
    app = create_app()
    
    with app.app_context():
        # Check if admin already exists
        admin_email = "admin@hbnb.com"
        existing_admin = facade.get_user_by_email(admin_email)
        
        if existing_admin:
            print(f"Admin user already exists: {admin_email}")
            print(f"Admin ID: {existing_admin.id}")
            return existing_admin
        
        # Create admin user
        admin_data = {
            'first_name': 'Admin',
            'last_name': 'User',
            'email': admin_email,
            'password': 'admin123',
            'is_admin': True
        }
        
        admin_user = facade.create_user(admin_data)
        print(f"Admin user created successfully!")
        print(f"Email: {admin_user.email}")
        print(f"Password: admin123")
        print(f"Admin ID: {admin_user.id}")
        print(f"Is Admin: {admin_user.is_admin}")
        
        return admin_user

if __name__ == '__main__':
    create_admin_user()
