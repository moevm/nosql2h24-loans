from weakref import ref
from flask import Blueprint, request, jsonify, send_file
from models import Client, Admin, Credit, CreditRequest
from mongoengine import connect
import json
from io import BytesIO
import logging

bp = Blueprint('statistic_routes', __name__)
connect(db="credit_database", host="localhost", port=27017)

# def count_rating(client_id):
#     counted_rating = 0
#     client = Client.objects(_id=client_id).first()
#     if client.workplace is not "":
#         counted_rating += 30 
#     else:
#         counted_rating -= 50
#     counted += (client.salary / 390000)
#     if client.amount_of_children > 0:
#         counted_rating -= 5 * client.amount_of_children
#     if client.marital_status == "married" and client.spouse_workplace is not "":
#         counted_rating += (client.spouse_salary / 520000)
#     for house in client.owned_property:
#         counted_rating += house.value / 13000000 
#     for history in client.credit_history:
#         if history.status == "closed":
#             counted_rating += 5 / 13 
#         elif history.status == "expired":
#             counted_rating -= 10 / 13
#         elif history.status == "opened":
#             counted_rating -= 5 / 13
#             credit = Credit.objects(_id=history.loan_id).first()
#             count_rating += (credit.deposit / 260000) 
#             #if credit.co_borrowers:
#              #   for coborrower in credit.co_borrowers:
#               #      count_rating += (coborrower.salary / 650000) 
    
#     if counted_rating > 10:
#         counted_rating = 10
#     if counted_rating < 0:
#         counted_rating = 0
#     print(counted_rating, "рейтинг гомяка")
#     client.rating = round(counted_rating, 1)
#     client.update_one(rating=counted_rating)


@bp.route('/database_export', methods=['GET'])
def export_database():
    print('hererherhehrehrehre')
    collections = {
        "clients": Client.objects,
        "admins": Admin.objects,
        "credits": Credit.objects,
        "credit_requests": CreditRequest.objects
    }
    data_dump = {}
    for name, collection in collections.items():
        data_dump[name] = [doc.to_mongo().to_dict() for doc in collection]
        
    json_data = json.dumps(data_dump, default=str)

    json_file = BytesIO(json_data.encode('utf-8'))
    json_file.seek(0)

    print("Дамп данных сохранен в JSON файл")
    return send_file(json_file, mimetype='application/json', as_attachment=True, download_name='data_dump.json')


@bp.route('/database_import', methods=['POST'])
def import_database():
    if 'file' not in request.files:
        return jsonify({"message": "Файл не найден"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "Не удалось загрузить файл"}), 400
    
    print(f"Чтение дампа из файла:", file.filename)
    data = json.load(file)
    
    for client_data in data.get("clients", []):
        Client(**client_data).save()
    for admin_data in data.get("admins", []):
        Admin(**admin_data).save()
    for credit_data in data.get("credits", []):
        Credit(**credit_data).save()
    for credit_request_data in data.get("credit_requests", []):
        CreditRequest(**credit_request_data).save()
    print("Данные успешно загружены из дампа")
    return jsonify({"adminName": Admin.objects(_id=request.form.get('user_id')).first().name, "message": "Данные успешно загружены из дампа" }), 200