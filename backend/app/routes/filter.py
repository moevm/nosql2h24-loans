from flask import Blueprint, request, jsonify, redirect, url_for
from models import CreditRequest, Credit, CreditHistory, Client, Admin
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
                "_id": str(req._id),
                "client_id": str(req.client_id),
                "loan_name": credit.loan_name,
                "request_time": req.request_time,
                "status": req.status,
                "amount": credit.amount,
                "interest_rate": credit.interest_rate,
                "expiration_time": credit.expiration_time
            })

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
                "request_time": req.request_time,
                "status": req.status,
                "amount": credit.amount,
                "interest_rate": credit.interest_rate,
                "rating": client.rating,
                "expiration_time": credit.expiration_time
            })
    
    if sort_direction != 0:
        result = sorted(result, key=lambda x: x[sort_field], reverse=(sort_direction == -1))
    return jsonify(result), 200


@bp.route('/sort_active_credits', methods=['GET'])
def sort_credit():
    print('Пришел запрос на сортировку Credit со следующими аргументами:', request.args)
    
    client_id = request.args.get("client_id")
    sort_field = request.args.get('sort_field')
    sort_direction = int(request.args.get('sort_direction', 0))
    
    credit_requests = CreditRequest.objects(client_id=client_id)
    # Получение информации о кредитах
    result = []
    for req in credit_requests:
        credit = Credit.objects(_id=req.loan_id).first()
        if credit and req.status == 'approved':
            result.append({
                "_id": str(req.loan_id),
                "loan_name": credit.loan_name,
                'opening_date': credit.opening_date,
                'expiration_time': credit.expiration_time,
                'amount': credit.amount,
                'interest_rate': credit.interest_rate,
                'monthly_payment': credit.monthly_payment,
                'next_payment_date': credit.next_payment_date,
                'debt': credit.debt,
                'payments_overdue': credit.payments_overdue,
            })
            
    # Сортировка
    if sort_direction != 0:
        result = sorted(result, key=lambda x: x[sort_field], reverse=(sort_direction == -1))

    return jsonify(result), 200


@bp.route('/sort_interaction_history', methods=['GET'])
def sort_interaction_history():
    print('Пришел запрос на сортировку CreditHistory со следующими аргументами:', request.args)
    
    admin_id = request.args.get("admin_id")
    sort_field = request.args.get('sort_field')
    sort_direction = int(request.args.get('sort_direction', 0))
    
    admin = Admin.objects(_id=admin_id).first()
    if not admin:
        return jsonify({"message" : "Администратор не найден"}), 200
    result = []
    for history in admin.interaction_history:
        credit_request = CreditRequest.objects(_id=history.credit_request_id).first()
        if credit_request:
            client = Client.objects(_id=credit_request.client_id).first()
            credit = Credit.objects(_id=credit_request.loan_id).first()
            if credit and credit_request.status != "processing":
                result.append({
                    "client_id": str(client._id),
                    "fio": client.name,
                    "loan_name": credit.loan_name,
                    "request_time": credit_request.request_time,
                    "processing_date": history.processing_date,
                    "amount": credit.amount,
                    "interest_rate": credit.interest_rate,
                    "expiration_time": credit.expiration_time,
                    "rating": client.rating,
                    "decision": history.decision
                })
    
    # Сортировка
    if sort_direction != 0:
        result = sorted(result, key=lambda x: x[sort_field], reverse=(sort_direction == -1))
    
    return jsonify(result), 200


@bp.route('/sort_user_credit_history', methods=['GET'])
def sort_user_credit_history():
    print('Пришел запрос на сортировку кредитной истории конкретного пользователя со следующими данными', request.args)
    
    client_id = request.args.get("client_id")
    sort_field = request.args.get('sort_field')
    sort_direction = int(request.args.get('sort_direction', 0))
    
    client = Client.objects(_id=client_id).first()
    if not client:
        return jsonify({"message": "Клиент не найден"})
    
    result = []
    for history in client.credit_history:
        current_credit = Credit.objects(_id=history.loan_id).first()
        if current_credit:
            result.append({
                "loan_name": current_credit.loan_name,
                "opening_date": current_credit.opening_date,
                "amount": current_credit.amount,
                "interest_rate": current_credit.interest_rate,
                "expiration_time": current_credit.expiration_time,
                "monthly_payment": current_credit.monthly_payment,
                "next_payment_date": current_credit.next_payment_date,
                "debt": current_credit.debt,
                "payments_overdue": current_credit.payments_overdue,
                "status": history.status
            })
    
    # Сортировка
    if sort_direction != 0:
        result = sorted(result, key=lambda x: x[sort_field], reverse=(sort_direction == -1))
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
        
    if not credit_query_filter and not query_filter:
        credit_requests = CreditRequest.objects(client_id=client_id)
        response_data = []
        for req in credit_requests:
            credit_info = Credit.objects.get(_id=req.loan_id)
            response_data.append({
                '_id': str(req._id),
                'client_id': str(req.client_id),
                'loan_id': str(req.loan_id),
                'request_time': req.request_time,
                'status': req.status,
                'loan_name': credit_info.loan_name,
                'amount': credit_info.amount,
                'interest_rate': credit_info.interest_rate,
                'expiration_time': credit_info.expiration_time,
            })
            
        return jsonify(response_data), 200    
    filtered_requests_final = CreditRequest.objects(**query_filter)

    response_data = []
    
    for req in filtered_requests_final:
        credit_info = Credit.objects.get(_id=req.loan_id)
        response_data.append({
            '_id': str(req._id),
            'client_id': str(req.client_id),
            'loan_id': str(req.loan_id),
            'request_time': req.request_time,
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
            'request_time': req.request_time,
            'request_id': str(req._id),
            'rating': user_info.rating,
            'client_id': str(user_info._id),
            'loan_name': credit_info.loan_name,
            'amount': credit_info.amount,
            'interest_rate': credit_info.interest_rate,
            'expiration_time': credit_info.expiration_time,
        })

    return jsonify(response_data), 200


@bp.route("/filter_active_credits", methods=['GET'])
def filter_active_credits():
    print("Пришел запрос на фильтрацию активных кредитов", request.args)
    data = request.args
    credit_query_filter = {}
    print(data.get('loan_name').split('@'))
    
    if data.get('loan_name'):
        credit_query_filter['loan_name__in'] = data['loan_name'].split('@')
    if data.get('amount_from'):
        credit_query_filter['amount__gte'] = float(data['amount_from'])
    if data.get('amount_to'):
        credit_query_filter['amount__lte'] = float(data['amount_to'])
    if data.get('interest_rate_from'):
        credit_query_filter['interest_rate__gte'] = float(data['interest_rate_from'])
    if data.get('interest_rate_to'):
        credit_query_filter['interest_rate__lte'] = float(data['interest_rate_to'])
    if data.get('expiration_time_from'):
        credit_query_filter['expiration_time__gte'] = int(data['expiration_time_from']) 
    if data.get('expiration_time_to'):
        credit_query_filter['expiration_time__lte'] = int(data['expiration_time_to'])
    if data.get('opening_date_from'):
        credit_query_filter['opening_time__gte'] = datetime.fromisoformat(data['opening_date_from'])
    if data.get('opening_date_to'):
        credit_query_filter['opening_time__lte'] = datetime.fromisoformat(data['opening_date_to'])
    if data.get('monthly_payment_from'):
        credit_query_filter['monthly_payment__gte'] = int(data['monthly_payment_from'])
    if data.get('monthly_payment_to'):
        credit_query_filter['monthly_payment__lte'] = int(data['monthly_payment_to'])
    if data.get('next_payment_date_from'):
        credit_query_filter['next_payment_date__gte'] = datetime.fromisoformat(data['next_payment_date_from'])
    if data.get('next_payment_date_to'):
        credit_query_filter['next_payment_date__lte'] = datetime.fromisoformat(data['next_payment_date_to'])
    if data.get('debt_from'):
        credit_query_filter['debt__gte'] = int(data['debt_from'])
    if data.get('debt_to'):
        credit_query_filter['debt__lte'] = int(data['debt_to'])
    if data.get('payments_overdue_from'):
        credit_query_filter['payment_overdue__gte'] = int(data['payments_overdue_from'])
    if data.get('payment_overdue_to'):
        credit_query_filter['payments_overdue_to'] = int(data['payments_overdue_to'])

    filtered_credits = Credit.objects(**credit_query_filter)

    if not filtered_credits:
        return jsonify({}), 200

    loan_ids = [credit._id for credit in filtered_credits]

    response_data = []
    
    for history in Client.objects(_id=data['client_id']).first().credit_history:
        if history.loan_id in loan_ids and ( history.status == "opened" or history.status == "expired" ):
            credit = Credit.objects(_id=history.loan_id).first()
            response_data.append ({
               "_id" : str(history.loan_id),
               "loan_name" : credit.loan_name,
               "opening_date" :  credit.opening_date,
               "expiration_time" : credit.expiration_time,
               "amount" : credit.amount,
               "interest_rate" : credit.interest_rate,
               "monthly_payment" : credit.monthly_payment,
               "next_payment_date" : credit.next_payment_date,
               "debt" : credit.debt,
               "payments_overdue" : credit.payments_overdue,
            })

    return jsonify(response_data), 200
    
    
@bp.route("/filter_credit_history", methods=['GET'])
def filter_history():
    data = request.args
    print("Пришел запрос на фильтрацию истории кредитов со следующими параметрами", data)
    client_id = data.get('client_id')
    
    credit_query_filter = {}
    if data.get('loan_name'):
        credit_query_filter['loan_name__in'] = data['loan_name'].split('@')
    if data.get('opening_date_from'):
        credit_query_filter['opening_date__gte'] = datetime.fromisoformat(data['opening_date_from'])
    if data.get('opening_date_to'):
        credit_query_filter['opening_date__lte'] = datetime.fromisoformat(data['opening_date_to'])
    if data.get('amount_from'):
        credit_query_filter['amount__gte'] = float(data['amount_from'])
    if data.get('amount_to'):
        credit_query_filter['amount__lte'] = float(data['amount_to'])
    if data.get('interest_rate_from'):
        credit_query_filter['interest_rate__gte'] = float(data['interest_rate_from'])
    if data.get('interest_rate_to'):
        credit_query_filter['interest_rate__lte'] = float(data['interest_rate_to'])
    if data.get('expiration_time_from'):
        credit_query_filter['expiration_time__gte'] = int(data['expiration_time_from']) 
    if data.get('expiration_time_to'):
        credit_query_filter['expiration_time__lte'] = int(data['expiration_time_to'])
    if data.get('monthly_payment_from'):
        credit_query_filter['monthly_payment__gte'] = float(data['monthly_payment_from'])
    if data.get('monthly_payment_to'):
        credit_query_filter['monthly_payment__lte'] = float(data['monthly_payment_to'])
    if data.get('next_payment_date_from'):
        credit_query_filter['next_payment_date__gte'] = datetime.fromisoformat(data['next_payment_date_from'])
    if data.get('next_payment_date_to'):
        credit_query_filter['next_payment_date__lte'] = datetime.fromisoformat(data['next_payment_date_to'])
    if data.get('debt_from'):
        credit_query_filter['debt__gte'] = int(data['debt_from'])
    if data.get('debt_to'):
        credit_query_filter['debt__lte'] = int(data['debt_to'])
    if data.get('payments_overdue_from'):
        credit_query_filter['payments_overdue__gte'] = int(data['payments_overdue_from'])
    if data.get('payments_overdue_to'):
        credit_query_filter['payments_overdue__lte'] = int(data['payments_overdue_to'])
    filtered_credits = Credit.objects(**credit_query_filter)
    loan_ids = [credit._id for credit in filtered_credits]
    response_data = []
    for history in Client.objects(_id=client_id).first().credit_history:
        credit = Credit.objects(_id=history.loan_id).first()
        if credit._id in loan_ids and (data['status'] == '' or history.status in data.get('status').split('@')):
            response_data.append({
               "loan_name" : credit.loan_name,
               "opening_date" :  credit.opening_date,
               "expiration_time" : credit.expiration_time,
               "amount" : credit.amount,
               "interest_rate" : credit.interest_rate,
               "monthly_payment" : credit.monthly_payment,
               "next_payment_date" : credit.next_payment_date,
               "debt" : credit.debt,
               "payments_overdue" : credit.payments_overdue,
               "status" : history.status
            })
    print(response_data)
    return jsonify(response_data), 200
        

@bp.route("/filter_interaction_history", methods=['GET'])
def filter_interaction_history():
    data = request.args
    print("Пришел запрос на фильтрацию истории взаимодействий со следующими параметрами", data)
    admin_id = data['admin_id']
    client_query_filter = {}
    credit_query_filter = {}
    credit_request_filter = {}
    if data.get('fio'):
        client_query_filter['name__icontains'] = data['fio']
    if data.get('rating_from'):
        client_query_filter['rating__gte'] = data['rating_from']
    if data.get('rating_to'):
        client_query_filter['rating__lte'] = data['rating_to']
    filtered_users = Client.objects(**client_query_filter)
    if data.get('loan_name'):
        credit_query_filter['loan_name__in'] = data['loan_name'].split('@')
    if data.get('amount_from'):
        credit_query_filter['amount__gte'] = data['amount_from']
    if data.get('amount_to'):
        credit_query_filter['amount__lte'] = data['amount_to']
    if data.get('interest_rate_from'):
        credit_query_filter['interest_rate__gte'] = float(data['interest_rate_from'])
    if data.get('interest_rate_to'):
        credit_query_filter['interest_rate__lte'] = float(data['interest_rate_to'])
    if data.get('expiration_time_from'):
        credit_query_filter['expiration_time__gte'] = int(data['expiration_time_from']) 
    if data.get('expiration_time_to'):
        credit_query_filter['expiration_time__lte'] = int(data['expiration_time_to'])
    filtered_credits = Credit.objects(**credit_query_filter)
    
    client_ids = [client._id for client in filtered_users]
    loan_ids = [loan._id for loan in filtered_credits]
    
    credit_request_filter['client_id__in'] = client_ids
    credit_request_filter['loan_id__in'] = loan_ids
    if data.get('request_time_from'):
        credit_request_filter['request_time__gte'] = datetime.fromisoformat(data['request_time_from'])
    if data.get('request_time_to'):
        credit_request_filter['request_time__lte'] = datetime.fromisoformat(data['request_time_to'])
    filtered_requests = CreditRequest.objects(**credit_request_filter)
    request_ids = [request._id for request in filtered_requests]
    
    decision_array = []
    if data.get('decision'):
        decision_array = data['decision'].split('@')
        for i in range(len(decision_array)):
            if decision_array[i] == "true":
                decision_array[i] = True
            else:
                decision_array[i] = False
    response_data = []
    
    for interaction in Admin.objects(_id=admin_id).first().interaction_history:
        if (
            (data['decision'] == '' or interaction.decision in decision_array) and
            (data['processing_date_from'] == '' or interaction.processing_date >= datetime.fromisoformat(data.get('processing_date_from'))) and
            (data['processing_date_to'] == '' or interaction.processing_date <= datetime.fromisoformat(data.get('processing_date_to'))) and
            (interaction.credit_request_id in request_ids)
        ):
            credit_request = CreditRequest.objects(_id=interaction.credit_request_id).first()
            if credit_request:
                client = Client.objects(_id=credit_request.client_id).first()
                credit = Credit.objects(_id=credit_request.loan_id).first()
                if client and credit:
                    response_data.append({
                    "fio" : client.name,
                    "loan_name" : credit.loan_name,
                    "client_id" : str(client._id),
                    "request_time" : credit_request.request_time,
                    "processing_date" : interaction.processing_date,
                    "amount" : credit.amount,
                    "interest_rate" : credit.interest_rate,
                    "expiration_time" : credit.expiration_time,
                    "rating" : client.rating,
                    "decision" : interaction.decision 
                })
                    
    return jsonify(response_data), 200 