from .routes import Service_A, Service_B #, Service_C
from .auth import login
from flask_restful import Resource

def register_routes(api):
    api.add_resource(Service_A, '/service_A')       
    api.add_resource(Service_B, '/service_B/<int:id>/')
    #api.add_resource(Service_C, '/Service_C')   