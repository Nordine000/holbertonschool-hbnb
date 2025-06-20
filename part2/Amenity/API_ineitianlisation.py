# api/__init__.py
from flask_restx import Api
from api.v1.amenities import api as amenities_ns
# Import other namespaces as needed
# from api.v1.users import api as users_ns
# from api.v1.places import api as places_ns

api = Api(
    title='HBnB Evolution API',
    version='1.0',
    description='API for the HBnB Evolution application',
    doc='/api/v1/'
)

# Register namespaces
api.add_namespace(amenities_ns, path='/api/v1/amenities')
# api.add_namespace(users_ns, path='/api/v1/users')
# api.add_namespace(places_ns, path='/api/v1/places')
