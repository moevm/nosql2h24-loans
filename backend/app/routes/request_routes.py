from flask import Blueprint, request, jsonify
from models import CreditRequest, Credit
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
    collateral = data.get('collateral')
    
    if not client_id or not loan_type:
        return jsonify({"error": "client_id and loan_type are required"}), 400

    new_credit = Credit(_id=ObjectId("".join(random.choices(string.hexdigits.lower(), k=24))), loan_name=loan_type, amount=loan_amount, interest_rate=5.5, deposit=collateral, co_borrowers=co_borrowers.split(', '), expiration_time=expiration_time).save()

    credit_request = CreditRequest(
        _id=ObjectId("".join(random.choices(string.hexdigits.lower(), k=24))),
        client_id=client_id,
        loan_id=new_credit._id,
        request_time = datetime.utcnow(),
        status="processing"
    )
    credit_request.save()
    return jsonify({"message": "Credit request created successfully", "request_id": str(credit_request.id)}), 201

# (`http://127.0.0.1:5000/credit_request?client_id=${userId}`);
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
