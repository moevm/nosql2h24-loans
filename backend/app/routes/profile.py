from flask import Blueprint, request, jsonify
from models import Client, Admin, Property
from mongoengine import ObjectIdField
from datetime import datetime
from bson import ObjectId
from utils.validation import *
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
            
        first_name, last_name, middle_name = user.name.split(' ')
        birthdate = getattr(user, 'birthdate', '')
        if birthdate:
            birthdate = birthdate.strftime('%Y-%m-%d')
        
        properties = [prop.to_dict() for prop in getattr(user, 'owned_property', [])]
        
        profile_data = {
            "firstName": first_name,
            "lastName": last_name,
            "middleName": middle_name,
            "email": getattr(user, 'email', ''),
            "passportNumber": getattr(user, 'passport_number', ''),
            'passportSeries': getattr(user, "passport_series", ''),
            "workplace": getattr(user, 'workplace', ''),
            "post": getattr(user, 'post', ''),
            "gender": getattr(user, 'sex', ''),
            "birthdate": birthdate,
            "contactPhone": getattr(user, 'phone', ''),
            "familyStatus": getattr(user, 'marital_status', ''),
            "childrenCount": getattr(user, 'amount_of_children', ''),
            "income": getattr(user, 'salary', ''),
            "incomeSpouse": getattr(user, 'spouse_salary', ''),
            "workplaceSpouse": getattr(user, 'spouse_workplace', ''),
            "postSpouse": getattr(user, "spouse_post", ''),
            "properties": properties,
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
    print("Пришел запрос на изменение данных для клиента:", data)

    # Парсинг переданных значений
    client_id = data.get("client_id")
    first_name = data.get("firstName") # имя
    last_name = data.get("lastName") # фамилия
    middle_name = data.get("middleName") # отчество
    email = data.get("email")
    passport_series = data.get("passportSeries")
    passport_number = data.get("passportNumber")
    workplace = data.get("workplace")
    post = data.get("post")
    gender = data.get("gender")
    birthdate = data.get("birthdate")
    contactPhone = data.get("contactPhone")
    familyStatus = data.get("familyStatus")
    childrenCount = data.get("childrenCount")
    income = data.get("income")
    incomeSpouse = data.get("incomeSpouse")
    workplaceSpouse = data.get("workplaceSpouse")
    postSpouse = data.get("postSpouse")
    properties = data.get("properties")
    photo = data.get("photo")
    
    errors = []
    
    if not client_id or not ObjectId.is_valid(client_id):
        errors.append("Неверный client_id.")
    if re.search(r'\d', first_name):
        errors.append("Имя не должно содержать числа.")
    if re.search(r'\d', last_name):
        errors.append("Фамилия не должна содержать числа.")
    if re.search(r'\d', middle_name):
        errors.append("Отчество не должно содержать числа.")
    if email and not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        errors.append("Некорректный вид email.")
    if contactPhone and not validate_phone_number(contactPhone):
        errors.append("Некорректный формат телефона.")
    if properties:
        for property in properties:
            current_type = property.get('type')
            current_value = property.get('value')
            current_legal = property.get('legal')
            if not(current_type and current_value and current_legal):
                errors.append(f"Имущество со следующими значениями: {current_type}, {current_value}, {current_legal} некорректно.")
    if childrenCount and childrenCount < 0:
        errors.append("Количество детей не может быть отрицательным числом.")
    if income and income < 0:
        errors.append("Заработная плата не может быть отрицательным числом.")
    if incomeSpouse and incomeSpouse < 0:
        errors.append("Заработная плата супруга не может быть отрицательным числом.")
    if passport_number and not validate_passport_number(passport_number):
        errors.append("Номер паспорта должен иметь длину 6 и содержать исключительно числа.")
    if passport_series and not validate_passport_series(passport_series):
        errors.append("Серия паспорта должен иметь длину 4 и содержать исключительно числа.")
    
    if errors:
        print(errors)
        return jsonify({"error": "Validation failed", "details": errors}), 400
    
    client = Client.objects(_id=ObjectId(client_id)).first()
    if not client:
        return jsonify({"error": "Client not found"}), 404
    
    current_fio = client.name.split(' ')
    try:
        if first_name:
            current_fio[0] = first_name
        if last_name:
            current_fio[1] = last_name
        if middle_name:
            current_fio[2] = middle_name
        
        client.name = ' '.join(current_fio)
        if email:
            client.email = email
        if passport_number:
            client.passport_number = passport_number
        if passport_series:
            client.passport_series = passport_series
        if workplace:
            client.workplace = workplace
        if post:
            client.post = post
        if gender:
            client.sex = gender
        if birthdate:
            client.birthdate = datetime.strptime(birthdate, '%Y-%m-%d')
        if contactPhone:
            try:
                client.phone = contactPhone
            except Exception as e:
                errors = ["Номер телефона имеет некорректную длину или формат."]
                print(errors)
                return jsonify({"error": "Validation failed", "details": errors}), 400
        if familyStatus:
            client.marital_status = familyStatus
        if childrenCount is not None:
            client.amount_of_children = int(childrenCount)
        if income is not None:
            client.salary = float(income)
        if incomeSpouse is not None:
            client.spouse_salary = float(incomeSpouse)
        if workplaceSpouse:
            client.spouse_workplace = workplaceSpouse
        if postSpouse:
            client.spouse_post = postSpouse
        if properties:
            client.owned_property = []
            for property in properties:
                current_type = property.get('type')
                current_value = property.get('value')
                current_legal = property.get('legal')
                if current_type and current_value and current_legal:
                    exists = any(
                        p.type == current_type and p.value == current_value and p.legal == current_legal
                        for p in client.owned_property
                    )
                    if not exists:
                        client.owned_property.append(Property(type=current_type, value=current_value, legal=current_legal))
        if not properties:
            client.owned_property = []
        if photo:
            client.photo = photo
    except Exception as e:
        error_message = f"Произошла ошибка на сервере: {e}"
        print(error_message)
        return jsonify({"message": error_message}), 500
        
        
    client.save()
    
    return jsonify({"message": "Client profile updated successfully"}), 200