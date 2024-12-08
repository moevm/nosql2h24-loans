from flask import Blueprint, request, jsonify
from models import Client, Admin
from utils.auth import generate_token
from datetime import date
import random, string
from bson import ObjectId
import logging

logging.basicConfig(level=logging.INFO)

bp = Blueprint('auth_routes', __name__)

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    logging.info("Попытка входа со следующими данными: %s", data)
    logging.info("Клиенты " + str(Client.objects))
    admin = Admin.objects(email=email).first()
    client = Client.objects(email=email).first()
    
    if admin and admin.password == password:
        token = generate_token(str(admin.id))
        return jsonify({"message": "Admin logged in successfully",
                        "userId": str(admin.id),
                        "userType": "admin",
                        "token": token,
                        "userName": admin.name}), 200
    
    #print(client.password, password)
    if client and client.password == password:
        token = generate_token(str(client.id))
        return jsonify({"message": "Client logged in successfully",
                        "userId": str(client.id),
                        "userType": "client",
                        "token": token,
                        "userName": client.name}), 200
        
    return jsonify({"error": "Invalid email or password"}), 401


@bp.route("/register", methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    surname = data.get('surname')
    email = data.get('email')
    password = data.get('password')
    print("Попытка регистрации с данными", data)
    if Client.objects(email=email).first() == None:
        try:
            new_client = Client(
                _id = ObjectId("".join(random.choices(string.hexdigits.lower(), k=24))),
                name = surname + " " +name,
                email = email,
                workplace = "",
                sex = "",
                password = password,
                phone = "",
                age = 0,
                birthdate = date(2000, 1, 1),
                salary = 0,
                self_employment_status = "idle",
                owned_property = [],
                marital_status = "single",
                spouse_workplace = "",
                spouse_salary = 0,
                amount_of_children = 0,
                rating = 0,
                credit_history = []
            )
            
            new_client.save()
            
            return jsonify({"message": "Client registered in successfully"}), 200
        except Exception as e:
            print(e)
            return jsonify({"message": "Ошибка со стороны сервера"}), 404
    else:
        return jsonify({"message": "ОшибкаЭ пользователь с такой почтой существует"}), 401
