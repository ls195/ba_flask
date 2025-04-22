from .routes import Kunde_list, Kunde_add, Get_max_kd_nr, Service_A, Service_B
from .auth import login
from flask_restful import Resource

def register_routes(api):
    api.add_resource(Kunde_list, '/api/kunden/list')                #gibt auskunft über alle Kunden {"kd_nr": XYZ, "vorname": "Maximilian"}
    api.add_resource(Get_max_kd_nr, '/api/kunden/get_max_kd_nr')
    api.add_resource(Kunde_add, '/api/kunden/add')
    api.add_resource(Service_A, '/api/service/A')
    api.add_resource(Service_B, '/api/service/B/<int:id>')