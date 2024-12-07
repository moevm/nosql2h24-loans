from flask import Blueprint, request, jsonify, send_file
from models import Client, Admin, Credit, CreditRequest
from mongoengine import connect
import json
from io import BytesIO

bp = Blueprint('statistic_routes', __name__)
connect(db="credit_database", host="localhost", port=27017)


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
    return jsonify({"message": "Данные успешно загружены из дампа"}), 200