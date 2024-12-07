from flask import Blueprint, request, jsonify
from models import CreditRequest, Credit, CreditHistory, Client
from datetime import datetime
bp = Blueprint('filter_routes', __name__)


@bp.route('/sort_credit_request', methods=['GET'])
def sort_credit_request():
    print('Пришел запрос на сортировку CreditRequest со следующими аргументами:', request.args)
    
    # получение параметров
    client_id = request.args.get('client_id')
    sort_field = request.args.get('sort_field')
    sort_direction = int(request.args.get('sort_direction', 0))
    # sort_params = {
    #     'request_time': int(request.args.get('request_time', 0)),
    #     'status': int(request.args.get('status', 0)),
    #     'loan_name': int(request.args.get('loan_name', 0)),
    #     'amount': int(request.args.get('amount', 0)),
    #     'interest_rate': int(request.args.get('interest_rate', 0)),
    #     'expiration_time': int(request.args.get('expiration_time', 0))
    # }
    
    credit_requests = CreditRequest.objects(client_id=client_id)

    # Получение информации о кредитах
    result = []
    for req in credit_requests:
        credit = Credit.objects(_id=req.loan_id).first()
        if credit:
            result.append({
                "client_id": str(req.client_id),
                "loan_name": credit.loan_name,
                "request_time": req.request_time.isoformat(),
                "status": req.status,
                "amount": credit.amount,
                "interest_rate": credit.interest_rate,
                "expiration_time": credit.expiration_time
            })
            
    # Сортировка
    # for param, order in sort_params.items():
    #     if order != 0:
    #         result = sorted(result, key=lambda x: x[param], reverse=(order == -1))
    if sort_direction != 0:
        result = sorted(result, key=lambda x: x[sort_field], reverse=(sort_direction == -1))
    return jsonify(result), 200


@bp.route('/sort_credit', methods=['GET'])
def sort_credit():
    print('Пришел запрос на сортировку Credit со следующими аргументами:', request.args)
    
    #получение параметров
    client_id = request.args.get('client_id')
    sort_params = {
        'loan_name': int(request.args.get('loan_name', 0)),
        'opening_date': int(request.args.get('opening_date', 0)),
        'expiration_time': int(request.args.get('expiration_time', 0)),
        'amount': int(request.args.get('amount', 0)),
        'interest_rate': int(request.args.get('interest_rate', 0)),
        'monthly_payment': int(request.args.get('monthly_payment', 0)),
        'next_payment_date': int(request.args.get('next_payment_date', 0)),
        'debt': int(request.args.get('debt', 0)),
        'payments_overdue': int(request.args.get('payments_overdue', 0))
    }
    
    credit_requests = CreditRequest.objects(client_id=client_id)

    # Получение информации о кредитах
    result = []
    for req in credit_requests:
        credit = Credit.objects(_id=req.loan_id).first()
        if credit and credit.status == 'approved':
            result.append({
                "client_id": str(req.client_id),
                "loan_name": credit.loan_name,
                'opening_date': credit.opening_date.isoformat(),
                'expiration_time': credit.expiration_time,
                'amount': credit.amount,
                'interest_rate': credit.interest_rate,
                'monthly_payment': credit.monthly_payment,
                'next_payment_date': credit.next_payment_date,
                'debt': credit.debt,
                'payments_overdue': credit.payments_overdue,
            })
            
    # Сортировка
    for param, order in sort_params.items():
        if order != 0 and result:
            result = sorted(result, key=lambda x: x[param], reverse=(order == -1))

    return jsonify(result), 200


@bp.route('/sort_interaction_history', methods=['GET'])
def sort_interaction_history():
    print('Пришел запрос на сортировку CreditHistory со следующими аргументами:', request.args)
    
    #получение параметров
    client_id = request.args.get('client_id')
    sort_params = {
        'loan_name': int(request.args.get('loan_name', 0)),
        'opening_date': int(request.args.get('opening_date', 0)),
        'expiration_time': int(request.args.get('expiration_time', 0)),
        'amount': int(request.args.get('amount', 0)),
        'interest_rate': int(request.args.get('interest_rate', 0)),
        'monthly_payment': int(request.args.get('monthly_payment', 0)),
        'debt': int(request.args.get('debt', 0)),
        'payments_overdue': int(request.args.get('payments_overdue', 0)),
        'status': int(request.args.get('status', 0))
    }
    
    credit_history = CreditHistory.objects(client_id=client_id)
    
    # Получение информации о кредитной истории
    result = []
    for req in credit_history:
        credit = Credit.objects(_id=req.loan_id).first()
        if credit:
            result.append({
                "client_id": str(req.client_id),
                "loan_name": credit.loan_name,
                'opening_date': credit.opening_date.isoformat(),
                'expiration_time': credit.expiration_time,
                'amount': credit.amount,
                'interest_rate': credit.interest_rate,
                'monthly_payment': credit.monthly_payment,
                'debt': credit.debt,
                'payments_overdue': credit.payments_overdue,
                'status': req.status
            })
            
    # Сортировка
    for param, order in sort_params.items():
        if order != 0 and result:
            result = sorted(result, key=lambda x: x[param], reverse=(order == -1))
            
    return jsonify(result), 200


@bp.route('/filter_credit_request', methods=['GET'])
def filter_credit_request():
    print('Пришел запрос на фильтрацию с параметрами:', request.args)
    data = request.args
    client_id = data.get('client_id')

    query_filter = {'client_id': client_id}
    
    credit_query_filter = {}
    print(data.get('loan_name').split('@'))
    if data.get('loan_name'):
        credit_query_filter['loan_name__in'] = data['loan_name'].split('@')
    if data.get('amount_from'):
        credit_query_filter['amount__gte'] = float(data['amount_from'])
    if data.get('amount_to'):
        credit_query_filter['amount__lte'] = float(data['amount_to'])
    if data.get('rate_from'):
        credit_query_filter['interest_rate__gte'] = float(data['rate_from'])
    if data.get('rate_to'):
        credit_query_filter['interest_rate__lte'] = float(data['rate_to'])
    if data.get('term_from'):
        credit_query_filter['expiration_time__gte'] = int(data['term_from']) 
    if data.get('term_to'):
        credit_query_filter['expiration_time__lte'] = int(data['term_to'])

    filtered_credits = Credit.objects(**credit_query_filter)

    if not filtered_credits:
        return jsonify({}), 200

    loan_ids = [credit._id for credit in filtered_credits]

    query_filter['loan_id__in'] = loan_ids
    if data.get('status'):
        query_filter['status__in'] = data['status'].split('@')
    if data.get('date_from'):
        query_filter['request_time__gte'] = datetime.fromisoformat(data['date_from'])
    if data.get('date_to'):
        query_filter['request_time__lte'] = datetime.fromisoformat(data['date_to'])
        
    filtered_requests_final = CreditRequest.objects(**query_filter)

    response_data = []
    
    for req in filtered_requests_final:
        credit_info = Credit.objects.get(_id=req.loan_id)
        response_data.append({
            '_id': str(req._id),
            'client_id': str(req.client_id),
            'loan_id': str(req.loan_id),
            'request_time': req.request_time.isoformat(),
            'status': req.status,
            'loan_name': credit_info.loan_name,
            'amount': credit_info.amount,
            'interest_rate': credit_info.interest_rate,
            'expiration_time': credit_info.expiration_time,
        })

    return jsonify(response_data), 200


@bp.route("/active_credits", methods=['POST'])
def filter_active_credits():
    filtered_data = request.get_json()
    user_id = filtered_data['user_id']
    user = Client._objects.find(_id=user_id)
    credit_filters = {}
    
    if 'loan_name__icontains' in filtered_data:
        credit_filters['loan_name__icontains'] = filtered_data['loan_name']
    if 'amount__icontains' in filtered_data:
        credit_filters['amount'] = int(filtered_data['amount'])
    if 'interest_rate__icontains' in filtered_data:
        credit_filters['interest_rate'] = int(filtered_data['interest_rate'])
    if 'expiration_time__icontains' in filtered_data:
        credit_filters['expiration_time'] = int(filtered_data['expiration_time'])
    if 'monthly_payment__icontains' in filtered_data:
        credit_filters['monthly_payment'] = int(filtered_data['monthly_payment'])
    if 'debt' in filtered_data:
        credit_filters['debt__icontains'] = int(filtered_data['debt'])
    if 'payments_overdue__icontains' in filtered_data:
        credit_filters['payments_overdue'] = int(filtered_data['payments_overdue'])
    
    approved_credit_ids = [
        credit_history.loan_id for credit_history in user.credit_history
        if credit_history.status == 'approved'
    ]
    credit_filters['_id__in'] = approved_credit_ids
    filtered_credits = Credit.objects(**credit_filters)
    result = [credit.to_mongo().to_dict() for credit in filtered_credits]

    return jsonify(result), 200
    

@bp.route("/filter_credit_history", methods=['POST'])
def filter_history():
    filtered_data = request.get_json()
    user_id = filtered_data['user_id']
    user = Client._objects.find(_id=user_id)
    credit_filters = {}
    
    if 'loan_name__icontains' in filtered_data:
        credit_filters['loan_name__icontains'] = filtered_data['loan_name']
    if 'amount__icontains' in filtered_data:
        credit_filters['amount'] = int(filtered_data['amount'])
    if 'interest_rate__icontains' in filtered_data:
        credit_filters['interest_rate'] = int(filtered_data['interest_rate'])
    if 'expiration_time__icontains' in filtered_data:
        credit_filters['expiration_time'] = int(filtered_data['expiration_time'])
    if 'monthly_payment__icontains' in filtered_data:
        credit_filters['monthly_payment'] = int(filtered_data['monthly_payment'])
    if 'debt' in filtered_data:
        credit_filters['debt__icontains'] = int(filtered_data['debt'])
    if 'payments_overdue__icontains' in filtered_data:
        credit_filters['payments_overdue'] = int(filtered_data['payments_overdue'])
    
    users_credit_ids = [ credit_history.loan_id for credit_history in user.credit_history ]
    credit_filters['_id__in'] = users_credit_ids
    filtered_credits = Credit.objects(**credit_filters)
    result = [credit.to_mongo().to_dict() for credit in filtered_credits]

    return jsonify(result), 200

@bp.route("/interaction_history", methods=['POST'])
def filter_interaction_history():
    pass


@bp.route("/filter_admins_request", methods=['POST'])
def filter_admins_request():
    pass