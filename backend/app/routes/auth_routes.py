from flask import Blueprint, request, jsonify
from models import Client, Admin
from utils.auth import generate_token
from werkzeug.security import check_password_hash
import jwt
import mongoengine

bp = Blueprint('auth_routes', __name__)

# @bp.route('/login/client', methods=['POST'])
# def client_login():
#     data = request.get_json()
#     email = data.get('email')
#     password = data.get('password')

#     client = Client.objects(email=email).first()
#     if client and check_password_hash(client.password, password):
#         return jsonify({"message": "Client logged in successfully", "client_id": str(client.id)}), 200
#     return jsonify({"error": "Invalid email or password"}), 401

# @bp.route('/login/admin', methods=['POST'])
# def admin_login():
#     data = request.get_json()
#     email = data.get('email')
#     password = data.get('password')

#     admin = Admin.objects(email=email).first()
#     if admin and check_password_hash(admin.password, password):
#         return jsonify({"message": "Admin logged in successfully", "admin_id": str(admin.id)}), 200
#     return jsonify({"error": "Invalid email or password"}), 401

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    print("Попытка входа со следующими данными:", data)
    
    # TODO: нужно исправить на сверку данных с БД
    admin = Admin.objects(email=email).first()
    client = Client.objects(email=email).first()
    
    # TODO: исправить хардкод почты
    if email == "admin@example.com":
        token = generate_token('1')
        return jsonify({"message": "Admin logged in successfully",
                        "userId": str(1),
                        "userType": "admin",
                        "token": token}), 200
    if email == "client@example.com":
        token = generate_token('1')
        return jsonify({"message": "Client logged in successfully",
                        "userId": str(1),
                        "userType": "client",
                        "token": token}), 200
    
    if admin and check_password_hash(admin.password, password):
        token = generate_token(str(admin.id))
        return jsonify({"message": "Admin logged in successfully",
                        "userId": str(admin.id),
                        "userType": "admin",
                        "token": token}), 200
        
    if client and check_password_hash(client.password, password):
        token = generate_token(str(client.id))
        return jsonify({"message": "Admin logged in successfully",
                        "userId": str(client.id),
                        "userType": "client",
                        "token": token}), 200
        
    return jsonify({"error": "Invalid email or password"}), 401

