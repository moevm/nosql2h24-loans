import json
from mongoengine import connect
from datetime import datetime
from bson import ObjectId
from ..backend.app.models import Credit, CreditHistory, CreditRequest, Client, Admin, InteractionHistory

connect(db="client_database", host="localhost", port=27017)

def create_sample_data():

    credits = [
        Credit(_id=ObjectId("64bfe2e30123456789abcdef"), loan_name="Молодежный", amount=5000, interest_rate=5.5, monthly_payment=150).save(),
        Credit(_id=ObjectId("64bfe2e40123456789abcdef"), loan_name="Эконом", amount=15000, interest_rate=4.2, monthly_payment=300).save(),
        Credit(_id=ObjectId("64bfe2e50123456789abcdef"), loan_name="Ипотека", amount=200000, interest_rate=3.8, monthly_payment=1200).save()
    ]

    credit_history = [
        CreditHistory(_id=ObjectId("64bfe2d10123456789abcdef"), loan_id=credits[0]._id, status="opened"),
        CreditHistory(_id=ObjectId("64bfe2d30123456789abcdef"), loan_id=credits[1]._id, status="closed", closing_date=datetime(2024, 10, 1)),
        CreditHistory(_id=ObjectId("64bfe2d50123456789abcdef"), loan_id=credits[2]._id, status="expired")
    ]
    
    clients = [
        Client(_id=ObjectId("64bfe2d70123456789abcdef"), name="John Doe", email="john@example.com", password="pass123", credit_history=credit_history[0]._id).save(),
        Client(_id=ObjectId("64bfe2d80123456789abcdef"), name="Jane Smith", email="jane@example.com", password="pass123", credit_history=credit_history[1]._id).save(),
        Client(_id=ObjectId("64bfe2d90123456789abcdef"), name="Alice Johnson", email="alice@example.com", password="pass123", credit_history=credit_history[2]._id).save()
    ]

    credit_requests = [
        CreditRequest(_id=ObjectId("64bfe2e60123456789abcdef"), client_id=clients[0]._id, loan_id=credits[0]._id, status="processing").save(),
        CreditRequest(_id=ObjectId("64bfe2e70123456789abcdef"), client_id=clients[1]._id, loan_id=credits[1]._id, status="approved").save(),
        CreditRequest(_id=ObjectId("64bfe2e80123456789abcdef"), client_id=clients[2]._id, loan_id=credits[2]._id, status="rejected").save()
    ]
    
    interaction_history = [
        InteractionHistory(_id=ObjectId("64bfe2da0123456789abcdef"), credit_request_id=credit_requests[0]._id, decision=True),
        InteractionHistory(_id=ObjectId("64bfe2dc0123456789abcdef"), credit_request_id=credit_requests[1]._id, decision=False),
        InteractionHistory(_id=ObjectId("64bfe2de0123456789abcdef"), credit_request_id=credit_requests[2]._id, decision=True)
    ]

    admins = [
        Admin(_id=ObjectId("64bfe2e00123456789abcdef"), name="Admin1", email="admin1@example.com", password="adminpass", interaction_history=interaction_history[0]._id).save(),
        Admin(_id=ObjectId("64bfe2e10123456789abcdef"), name="Admin2", email="admin2@example.com", password="adminpass", interaction_history=interaction_history[1]._id).save(),
        Admin(_id=ObjectId("64bfe2e20123456789abcdef"), name="Admin3", email="admin3@example.com", password="adminpass", interaction_history=interaction_history[2]._id).save()
    ]

    

def dump_data_to_json(output_file):
    collections = {
        "clients": Client.objects,
        "admins": Admin.objects,
        "credits": Credit.objects,
        "credit_requests": CreditRequest.objects
    }
    data_dump = {}
    for name, collection in collections.items():
        data_dump[name] = [doc.to_mongo().to_dict() for doc in collection]

    with open(output_file, 'w') as f:
        json.dump(data_dump, f, default=str)
    
    print(f"Дамп данных сохранен в файл {output_file}")

create_sample_data()
dump_data_to_json("mongo_dump.json")