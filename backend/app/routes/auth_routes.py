from flask import Blueprint, request, jsonify
from models import Client, Admin
from utils.auth import generate_token
import jwt
import mongoengine

bp = Blueprint('auth_routes', __name__)

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    print("Попытка входа со следующими данными:", data)
    
    admin = Admin.objects(email=email).first()
    client = Client.objects(email=email).first()
    
    if admin and admin.password == password:
        token = generate_token(str(admin.id))
        return jsonify({"message": "Admin logged in successfully",
                        "userId": str(admin.id),
                        "userType": "admin",
                        "token": token}), 200
    
    print(client.password, password)
    if client and client.password == password:
        token = generate_token(str(client.id))
        return jsonify({"message": "Client logged in successfully",
                        "userId": str(client.id),
                        "userType": "client",
                        "token": token}), 200
        
    return jsonify({"error": "Invalid email or password"}), 401

