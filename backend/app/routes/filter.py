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


@bp.route('/sort_admins_request', methods=['GET'])
def sort_credit_requests():
    print('Пришел запрос на сортировку CreditRequest у администратора со следующими аргументами:', request.args)
    
    # получение параметров
    sort_field = request.args.get('sort_field')
    sort_direction = int(request.args.get('sort_direction', 0))
    
    credit_requests = CreditRequest.objects(status="processing")

    # Получение информации о кредитах
    result = []
    for req in credit_requests:
        credit = Credit.objects(_id=req.loan_id).first()
        client = Client.objects(_id=req.client_id).first()
        if credit:
            result.append({
                "client_id": str(req.client_id),
                "request_id": str(req._id),
                "fio": client.name,
                "loan_name": credit.loan_name,
                "request_time": req.request_time.isoformat(),
                "status": req.status,
                "amount": credit.amount,
                "interest_rate": credit.interest_rate,
                "rating": client.rating,
                "expiration_time": credit.expiration_time
            })
    
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

@bp.route("/filter_admins_request", methods=['GET'])
def filter_admins_request():
    print('Пришел запрос на фильтрацию с параметрами:', request.args)
    data = request.args

    query_filter = {'status': 'processing'}
    client_filter = {}
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

    if data.get('fio'):
        client_filter['name__icontains'] = str(data['fio'])
    if data.get('rating_from'):
        client_filter['rating__gte'] = float(data['rating_from'])
    if data.get('rating_to'):
        client_filter['rating_lte'] = float(data['rating_to'])

    filtered_clients = Client.objects(**client_filter)

    if not filtered_credits:
        return jsonify({}), 200

    loan_ids = [credit._id for credit in filtered_credits]
    client_ids = [client._id for client in filtered_clients]

    query_filter['loan_id__in'] = loan_ids
    query_filter['client_id__in'] = client_ids
    if data.get('date_from'):
        query_filter['request_time__gte'] = datetime.fromisoformat(data['date_from'])
    if data.get('date_to'):
        query_filter['request_time__lte'] = datetime.fromisoformat(data['date_to'])
        
    filtered_requests_final = CreditRequest.objects(**query_filter)

    response_data = []
    
    for req in filtered_requests_final:
        credit_info = Credit.objects.get(_id=req.loan_id)
        user_info = Client.objects.get(_id=req.client_id)
        response_data.append({
            '_id': str(req._id),
            'client_id': str(req.client_id),
            'fio': user_info.name,
            'loan_id': str(req.loan_id),
            'request_time': req.request_time.isoformat(),
            'request_id': str(req._id),
            'rating': user_info.rating,
            'client_id': str(user_info._id),
            'loan_name': credit_info.loan_name,
            'amount': credit_info.amount,
            'interest_rate': credit_info.interest_rate,
            'expiration_time': credit_info.expiration_time,
        })

    return jsonify(response_data), 200


@bp.route("/active_credits", methods=['POST'])
def filter_active_credits():
    pass
    

@bp.route("/filter_credit_history", methods=['POST'])
def filter_history():
    pass

@bp.route("/interaction_history", methods=['POST'])
def filter_interaction_history():
    pass