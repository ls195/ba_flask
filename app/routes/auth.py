from flask import Blueprint, request, jsonify
from flask import current_app as app
from flask_jwt_extended import create_access_token

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=['POST'])              ##JWT Initialisierung über /login
def login():
    username = request.json.get('username', None)       ## Angelehnt an https://flask-jwt-extended.readthedocs.io/en/stable/basic_usage.html
    password = request.json.get('password', None)
    if username != 'test' or password != 'test':
        return jsonify({'Nicht authorisiert':' Benutzername oder Passwort ist falsch'}), 401
    access_token = create_access_token(identity = username)
    return jsonify({'access':access_token}) 

# return jsonify(access_token=access_token) 