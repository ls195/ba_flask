from flask import Flask
from flask_restful import Api
from .extensions import db, jwt, cache, api, ma
from .routes import register_routes
from flask_sqlalchemy import SQLAlchemy
# Konfiguration, Extension-Init, etc.
 
#print("hello")

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')          #https://flask.palletsprojects.com/en/stable/config/#configuring-from-python-files
    db.init_app(app)                                    #Extension Guidelines: https://flask.palletsprojects.com/en/stable/extensiondev/
    jwt.init_app(app)
    cache.init_app(app)
    api.init_app(app)
    ma.init_app(app)
    register_routes(api)

    

    
