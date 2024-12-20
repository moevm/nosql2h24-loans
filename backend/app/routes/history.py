from flask import Blueprint, request, jsonify
from routes.statistic import count_rating
from models import CreditRequest, Credit, Client, Admin, InteractionHistory
from utils.validation import *

bp = Blueprint('interaction_history_routes', __name__)

@bp.route('/get_interactions', methods=['GET'])
def get_interactions():
    data = request.args
    print("Пришел запрос на получение истории взаимодействий", data)
    admin_id = data.get('admin_id')
    admin = Admin.objects(_id=admin_id).first()
    if not admin:
        return jsonify({"message" : "Администратор не найден"}), 200
    response_data = []
    for history in admin.interaction_history:
        credit_request = CreditRequest.objects(_id=history.credit_request_id).first()
        if credit_request:
            client = Client.objects(_id=credit_request.client_id).first()
            credit = Credit.objects(_id=credit_request.loan_id).first()
            if client and credit:
                response_data.append({
                    "fio" : client.name,
                    "loan_name" : credit.loan_name,
                    "client_id" : str(client._id),
                    "request_time" : credit_request.request_time,
                    "processing_date" : history.processing_date,
                    "amount" : credit.amount,
                    "interest_rate" : credit.interest_rate,
                    "expiration_time" : credit.expiration_time,
                    "rating" : client.rating,
                    "decision" : history.decision 
                })
    return jsonify(response_data), 200
