from flask import Blueprint, request, jsonify
from models import Client, Admin
from mongoengine import ObjectIdField
from datetime import datetime
from bson import ObjectId
import re

bp = Blueprint('profile_routes', __name__)

@bp.route('/get_profile', methods=["GET"])
def get_user_profile():
    data = request.args
    print("Пришел запрос на получение информации профиля:", data)
    
    # Парсинг переданных значений
    user_id = data.get("userId")
    user_type = data.get("userType")
    if user_type == 'client':
        user = Client.objects(_id=ObjectId(user_id)).first()
        
        birthdate = getattr(user, 'birthdate', '')
        if birthdate:
            birthdate = birthdate.isoformat()
        
        profile_data = {
            "fio": getattr(user, 'name', ''),
            "email": getattr(user, 'email', ''),
            "workplace": getattr(user, 'workplace', ''),
            "gender": getattr(user, 'sex', ''),
            "birthdate": birthdate,
            "contactPhone": getattr(user, 'phone', ''),
            "familyStatus": getattr(user, 'marital_status', ''),
            "childrenCount": getattr(user, 'amount_of_children', ''),
            "income": getattr(user, 'salary', ''),
            "incomeSpouse": getattr(user, 'spouse_salary', ''),
            "workplaceSpouse": getattr(user, 'spouse_workplace', ''),
            "properties": getattr(user, 'owned_property', ''),
            "photo": getattr(user, 'photo', '')
        }
    elif user_type == 'admin':
        user = Admin.objects(_id=ObjectId(user_id)).first()
    else:
        return jsonify({"message": "User type doesn't provided"}), 400
    print(f"Данные профиля", profile_data)
    return jsonify(profile_data), 200

@bp.route('/client_profile_change', methods=['POST'])
def client_profile_change():
    data = request.get_json()
    print("Пришел запрос на изменение данных для пользователя")

    # Парсинг переданных значений
    client_id = data.get("client_id")
    fio = data.get("fio")
    email = data.get("email")
    workplace = data.get("workplace")
    gender = data.get("gender")
    birthdate = data.get("birthdate")
    contactPhone = data.get("contactPhone")
    familyStatus = data.get("familyStatus")
    childrenCount = data.get("childrenCount")
    income = data.get("income")
    incomeSpouse = data.get("incomeSpouse")
    workplaceSpouse = data.get("workplaceSpouse")
    properties = data.get("properties")
    photo = data.get("photo")
    
    errors = []
    
    if not client_id or not ObjectId.is_valid(client_id):
        errors.append("Invalid client_id")
    if fio and (not isinstance(fio, str) or len(fio.split()) != 3):
        errors.append("Invalid fio")
    if email and not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        errors.append("Invalid email")
    
    if errors:
        return jsonify({"error": "Validation failed", "details": errors}), 400
    
    client = Client.objects(_id=ObjectId(client_id)).first()
    if not client:
        return jsonify({"error": "Client not found"}), 404
    
    try:
        if fio:
            client.name = fio
        if email:
            client.email = email
        if workplace:
            client.workplace = workplace
        if gender:
            client.sex = gender
        if birthdate:
            client.birthdate = datetime.strptime(birthdate, '%Y-%m-%d')
        if contactPhone:
            client.phone = contactPhone
        if familyStatus:
            client.marital_status = familyStatus
        if childrenCount:
            client.amount_of_children = int(childrenCount)
        if income:
            client.salary = int(income)
        if incomeSpouse:
            client.spouse_salary = int(incomeSpouse)
        if workplaceSpouse:
            client.spouse_workplace = workplaceSpouse
        if properties:
            client.owned_property = properties
        if photo:
            client.photo = photo
    except Exception as e:
        error_message = f"Произошла ошибка на сервере: {e}"
        print(error_message)
        return jsonify({"message": error_message}), 500
        
        
    client.save()
    
    return jsonify({"message": "Client profile updated successfully"}), 200