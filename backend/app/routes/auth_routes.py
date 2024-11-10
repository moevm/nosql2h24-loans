from flask import Blueprint, request, jsonify
from models import Client, Admin
from werkzeug.security import check_password_hash
import mongoengine

bp = Blueprint('auth_routes', __name__)

@bp.route('/login/client', methods=['POST'])
def client_login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    client = Client.objects(email=email).first()
    if client and check_password_hash(client.password, password):
        return jsonify({"message": "Client logged in successfully", "client_id": str(client.id)}), 200
    return jsonify({"error": "Invalid email or password"}), 401

@bp.route('/login/admin', methods=['POST'])
def admin_login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    admin = Admin.objects(email=email).first()
    if admin and check_password_hash(admin.password, password):
        return jsonify({"message": "Admin logged in successfully", "admin_id": str(admin.id)}), 200
    return jsonify({"error": "Invalid email or password"}), 401
