from flask import Blueprint, request, jsonify
from models import CreditRequest, Credit, CreditHistory, Client, Coborrowers, Admin, InteractionHistory
from utils.validation import *
from mongoengine import ObjectIdField
from datetime import datetime
from bson import ObjectId
import random, string

bp = Blueprint('credit_request_routes', __name__)

@bp.route('/credit_request', methods=['POST'])
def create_credit_request():
    data = request.get_json()
    print(f"Пришел запрос на кредит: ", data)
    
    client_id = data.get('clientId')
    loan_type = data.get('loanType')
    loan_amount = data.get('loanAmount')
    expiration_time = data.get('expirationTime')
    co_borrowers = data.get('coBorrowers')
    deposit = data.get('deposit')
    
    errors = []
    if not deposit:
        errors.append("Должен быть указан залог.")
    else:
        deposit = int(deposit)
    if deposit and deposit < 0:
        errors.append("Залог не может быть отрицательной величиной.")
    if co_borrowers:
        for co_borrower in co_borrowers:
            current_post = co_borrower.get('post', None)
            current_workplace = co_borrower.get('workplace', None)
            current_name = co_borrower.get('fio', None)
            current_phone = co_borrower.get('contactPhone', None)
            current_passport_number = co_borrower.get('passportNumber', None)
            current_passport_series = co_borrower.get('passportSeries', None)
            if not current_name:
                errors.append("Имя созаемщика не указано.")
                break
            if not current_workplace:
                errors.append("Место работы созаемщика не указано.")
                break
            if not current_post:
                errors.append("Должность созаемщика не указана.")
                break
            if not current_phone:
                errors.append("Телефон созаемщика не указан.")
                break
            if not current_passport_number:
                errors.append("Номер паспорта созаемщика не указан.")
                break
            if not current_passport_series:
                errors.append("Серия паспорта созаемщика не указана.")
                break
            if not validate_phone_number(current_phone):
                errors.append("Некорректный формат телефона.")
            if not validate_passport_number(current_passport_number):
                errors.append("Серия паспорта должен иметь длину 6 и содержать исключительно числа.")
                break
            if not validate_passport_series(current_passport_series):
                errors.append("Серия паспорта должен иметь длину 4 и содержать исключительно числа.")
                break
            
        
    if errors:
        print(errors)
        return jsonify({"error": "Validation failed", "details": errors}), 400

    if not client_id or not loan_type:
        return jsonify({"error": "client_id and loan_type are required"}), 400

    new_credit = Credit(_id=ObjectId("".join(random.choices(string.hexdigits.lower(), k=24))), loan_name=loan_type, amount=loan_amount, interest_rate=5.5, deposit=deposit, 
                        co_borrowers=[Coborrowers(name=coborrower['fio'], workplace=coborrower['workplace'], phone=coborrower['contactPhone'], post=coborrower['post'], passport_number=coborrower['passportNumber'], passport_series=coborrower['passportSeries']) for coborrower in co_borrowers],
                        expiration_time=expiration_time).save()

    credit_request = CreditRequest(
        _id=ObjectId("".join(random.choices(string.hexdigits.lower(), k=24))),
        client_id=client_id,
        loan_id=new_credit._id,
        request_time = datetime.utcnow(),
        status="processing"
    )
    credit_request.save()
    return jsonify({"message": "Credit request created successfully", "request_id": str(credit_request.id)}), 201


@bp.route('/credit_request/', methods=['GET'])
def get_all_credit_requests():
    print("Пришел запрос на получение списка заявок на кредит:", request.args)
    client_id = request.args.get('client_id')
    credit_requests = CreditRequest.objects(client_id=client_id)
    result = [{"client_id": str(req.client_id), 
               "loan_name": Credit.objects(_id=req.loan_id).first().loan_name, 
               "request_time": req.request_time.isoformat(), 
               "status": req.status,
               "amount": Credit.objects(_id=req.loan_id).first().amount, 
               "interest_rate": Credit.objects(_id=req.loan_id).first().interest_rate,
               "expiration_time": Credit.objects(_id=req.loan_id).first().expiration_time} for req in credit_requests
            ]

    return jsonify(result), 200

@bp.route('/credit_request_decision', methods=['GET'])
def credit_request_decision():
    data = request.args
    print(f"Пришел запрос на решение заявки: ", data)
    status = data.get('decision')
    if status == 'true':
        status = "approved"
    else:
        status = "rejected"
    request_id = data.get('request_id')
    admin_id = data.get('admin_id')
    credit_request = CreditRequest.objects(_id=request_id).first()
    new_interaction = InteractionHistory(
        _id=ObjectId("".join(random.choices(string.hexdigits.lower(), k=24))),
        processing_date = datetime.utcnow(),
        credit_request_id = request_id,
        decision=status
    )
    
    credit_request.status = status
    credit_request.save()
    Admin.objects(_id=admin_id).update_one(push__interaction_history=new_interaction)#.save()
    if status == True:
        credit_history = CreditHistory(
            _id=ObjectId("".join(random.choices(string.hexdigits.lower(), k=24))),
            client_id=credit_request.client_id,
            loan_id=credit_request.loan_id,
            closing_time = None,
            status="opened"
        )
        credit_history.save()
        Client.objects(_id=credit_request.client_id).update_one(push__credit_history=credit_history)#.save()
        return jsonify({"message": "Credit request decision saved successfully"}), 200
    else:
        return jsonify({"message": "Credit request decision saved successfully"}), 200

@bp.route('/admins_request', methods=['GET'])
def admins_request():
    print("Пришел запрос на получение списка заявок на кредит:", request.args)
    credit_requests = CreditRequest.objects(status="processing")
    result = [{"client_id": str(req.client_id), 
               "request_id": str(req._id),
               "fio": Client.objects(_id=req.client_id).first().name,
               "rating": Client.objects(_id=req.client_id).first().rating,
               "loan_name": Credit.objects(_id=req.loan_id).first().loan_name, 
               "request_time": req.request_time.isoformat(), 
               "status": req.status,
               "amount": Credit.objects(_id=req.loan_id).first().amount, 
               "interest_rate": Credit.objects(_id=req.loan_id).first().interest_rate,
               "expiration_time": Credit.objects(_id=req.loan_id).first().expiration_time} for req in credit_requests
            ]
    print(result)
    return jsonify(result), 200