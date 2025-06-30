from .routes import Service_A, Service_B, Service_C
from .auth import login
from flask_restful import Resource

def register_routes(api):
    api.add_resource(Service_A, '/api/service/A')
    api.add_resource(Service_B, '/api/service/B/<int:id>')
    api.add_resource(Service_C, '/Service_C')