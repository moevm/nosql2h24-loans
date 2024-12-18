from flask import Blueprint, request, jsonify
from routes.statistic import count_rating
from models import CreditRequest, Credit, CreditHistory, Client, Coborrowers, Admin, InteractionHistory
from utils.validation import *
from utils.credit import generate_interest_rate
from mongoengine import ObjectIdField
from datetime import datetime
from bson import ObjectId
import random, string

bp = Blueprint('credit_request_routes', __name__)

@bp.route('/create_credit_request', methods=['POST'])
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

    interest_rate = generate_interest_rate(loan_name=loan_type, loan_amount=loan_amount, expiration_time=expiration_time)
    monthly_payment = round((1 + interest_rate / 100) * loan_amount / expiration_time, 2)
    new_credit = Credit(_id=ObjectId("".join(random.choices(string.hexdigits.lower(), k=24))),
                        loan_name=loan_type,
                        amount=loan_amount,
                        interest_rate=interest_rate,
                        deposit=deposit, 
                        monthly_payment=monthly_payment,
                        co_borrowers=[Coborrowers(name=coborrower['fio'], workplace=coborrower['workplace'], phone=coborrower['contactPhone'], post=coborrower['post'], passport_number=coborrower['passportNumber'], passport_series=coborrower['passportSeries']) for coborrower in co_borrowers],
                        expiration_time=expiration_time,
                        debt=loan_amount,
                        payments_overdue=0).save()

    credit_request = CreditRequest(
        _id=ObjectId("".join(random.choices(string.hexdigits.lower(), k=24))),
        client_id=client_id,
        loan_id=new_credit._id,
        request_time = datetime.utcnow(),
        status="processing"
    )
    credit_request.save()
    return jsonify({"message": "Credit request created successfully", "request_id": str(credit_request.id)}), 201


@bp.route('/get_credit_requests', methods=['GET'])
def get_all_credit_requests():
    print("Пришел запрос на получение списка заявок на кредит:", request.args)
    client_id = request.args.get('client_id')
    credit_requests = CreditRequest.objects(client_id=client_id)
    result = [{"client_id": str(req.client_id), 
               "_id": str(req._id),
               "loan_name": Credit.objects(_id=req.loan_id).first().loan_name, 
               "request_time": req.request_time.isoformat(), 
               "status": req.status,
               "amount": Credit.objects(_id=req.loan_id).first().amount, 
               "interest_rate": Credit.objects(_id=req.loan_id).first().interest_rate,
               "expiration_time": Credit.objects(_id=req.loan_id).first().expiration_time} for req in credit_requests
            ]

    return jsonify(result), 200


@bp.route('/get_active_credits', methods=["GET"])
def get_all_active_credits():
    print("Пришел запрос на получение активных кредитов пользователя:", request.args)
    client_id = request.args.get("client_id")
    credit_requests = CreditRequest.objects(client_id=client_id)
    result = []
    for req in credit_requests:
        if req and req.status == "approved":
            result.append({
                "_id": str(req.loan_id),
                "loan_name": Credit.objects(_id=req.loan_id).first().loan_name,
                "opening_date": Credit.objects(_id=req.loan_id).first().opening_date,
                "amount": Credit.objects(_id=req.loan_id).first().amount,
                "interest_rate": Credit.objects(_id=req.loan_id).first().interest_rate,
                "expiration_time": Credit.objects(_id=req.loan_id).first().expiration_time,
                "monthly_payment": Credit.objects(_id=req.loan_id).first().monthly_payment,
                "next_payment_date": Credit.objects(_id=req.loan_id).first().next_payment_date,
                "debt": Credit.objects(_id=req.loan_id).first().debt,
                "payments_overdue": Credit.objects(_id=req.loan_id).first().payments_overdue
            })
    
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
    if status == "approved":
        credit_history = CreditHistory(
            _id=ObjectId("".join(random.choices(string.hexdigits.lower(), k=24))),
            loan_id=credit_request.loan_id,
            closing_date = None,
            status="opened"
        )
        count_rating(credit_request.client_id)
        print("saved")
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
    # print(result)
    return jsonify(result), 200

@bp.route('/get_request_details', methods=['GET'])
def get_request_details():
    data = request.args
    print("Пришел запрос на показ заявки с данными", data)
    request_id = data.get('requestId')
    credit_request = CreditRequest.objects(_id=request_id).first()
    
    coborrowers = Credit.objects(_id=credit_request.loan_id).first().co_borrowers
    result = {
        "loan_name" : Credit.objects(_id=credit_request.loan_id).first().loan_name,
        "request_time" : credit_request.request_time,
        "deposit" : Credit.objects(_id=credit_request.loan_id).first().deposit,
        "status" : credit_request.status,
        "amount" : Credit.objects(_id=credit_request.loan_id).first().amount,
        "interest_rate" : Credit.objects(_id=credit_request.loan_id).first().interest_rate,
        "expiration_time": Credit.objects(_id=credit_request.loan_id).first().expiration_time,
        "co_borrowers": [coborrower.to_dict() for coborrower in coborrowers]
    }
    return jsonify(result), 200


@bp.route('/get_credit_details', methods=['GET'])
def get_credit_details():
    data = request.args
    print("Пришел запрос на показ заявки с данными", data)
    credit_id = data.get('creditId')
    credit = Credit.objects(_id=credit_id).first()
    
    result = {
        "loan_name" : credit.loan_name,
        "opening_date": credit.opening_date,
        "amount" : credit.amount,
        "interest_rate" : credit.interest_rate,
        "expiration_time": credit.expiration_time,
        "debt": credit.debt,
        "next_payment_date": credit.next_payment_date
    }
    return jsonify(result), 200