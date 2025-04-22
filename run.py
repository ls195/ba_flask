from flask import Flask
from flask_restful import Api
from app.extensions import db, jwt, cache
from app.routes.auth import auth_bp  # Importiere Blueprint
from app.routes import register_routes

app = Flask(__name__)
api = Api(app)
register_routes(api)
# Konfiguration, Extension-Init, etc.
app.config.from_object('app.config.Config')         #Extension Guidelines: https://flask.palletsprojects.com/en/stable/extensiondev/
#print("hello")
db.init_app(app)
jwt.init_app(app)
cache.init_app(app)

# Blueprint registrieren
app.register_blueprint(auth_bp)

if __name__ == '__main__':
    app.run(debug=True)