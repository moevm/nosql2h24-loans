from flask import Blueprint, request, jsonify
from models import CreditRequest
from mongoengine import ObjectIdField
from datetime import datetime

bp = Blueprint('credit_request_routes', __name__)

@bp.route('/credit_request', methods=['POST'])
def create_credit_request():
    data = request.get_json()
    client_id = data.get('client_id')
    loan_id = data.get('loan_id')
    
    print(f"Пришел запрос на кредит: ", data)
    
    if not client_id or not loan_id:
        return jsonify({"error": "client_id and loan_id are required"}), 400

    credit_request = CreditRequest(
        client_id=client_id,
        loan_id=loan_id,
        request_time=datetime.utcnow(),
        status="processing"
    )
    credit_request.save()
    return jsonify({"message": "Credit request created successfully", "request_id": str(credit_request.id)}), 201

@bp.route('/credit_requests', methods=['GET'])
def get_all_credit_requests():
    credit_requests = CreditRequest.objects()
    result = [{"client_id": str(req.client_id), 
               "loan_id": str(req.loan_id), 
               "request_time": req.request_time, 
               "status": req.status} for req in credit_requests]
    return jsonify(result), 200
