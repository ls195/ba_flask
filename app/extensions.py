from flask_restful import  Api
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from flask_jwt_extended import JWTManager
from flask_restful import Api

db = SQLAlchemy()
cache = Cache()
jwt = JWTManager()
api = Api()