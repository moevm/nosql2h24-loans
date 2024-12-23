import json
from mongoengine import connect
from datetime import datetime, timedelta
from bson import ObjectId
from models import Credit, CreditHistory, CreditRequest, Client, Admin, InteractionHistory, Property

# connect(host="mongodb://127.0.0.1:27017/credit_database")

def create_sample_data():

    credits = [
        Credit(
            _id=ObjectId("64bfe2e30123456789abcdef"),
            loan_name="Молодежный кредит",
            opening_date=datetime(2024, 9, 1),
            amount=500008,
            interest_rate=5.5,
            next_payment_date=datetime.now() + timedelta(days=10),
            monthly_payment=150,
            debt=100000,
            expiration_time=100,
            payments_overdue=0,
            co_borrowers=[],
            deposit=0
        ).save(),
        Credit(
            _id=ObjectId("64bfe2e40123456789abcdef"),
            loan_name="Автокредит",
            opening_date=datetime(2023, 8, 12),
            amount=150000,
            interest_rate=4.2,
            next_payment_date=datetime.now() + timedelta(days=15),
            monthly_payment=300,
            debt=10000,
            expiration_time=100,
            payments_overdue=2,
            co_borrowers=[],
            deposit=100
        ).save(),
        Credit(
            _id=ObjectId("64bfe2e50123456789abcdef"),
            loan_name="Ипотека",
            opening_date=datetime(2022, 10, 15),
            amount=2000000,
            interest_rate=3.8,
            next_payment_date=datetime.now() + timedelta(days=20),
            monthly_payment=1200,
            debt=10000,
            expiration_time=200,
            payments_overdue=1,
            co_borrowers=[],
            deposit=1020
        ).save(),
        Credit(
            _id=ObjectId("64bfe2e40123466789abcdef"),
            loan_name="Автокредит",
            opening_date=datetime(2021, 5, 1),
            amount=150000,
            interest_rate=4.2,
            next_payment_date=datetime.now() + timedelta(days=7),
            monthly_payment=300,
            debt=10000,
            expiration_time=100,
            payments_overdue=0,
            co_borrowers=[],
            deposit=20
        ).save(),
        Credit(
            _id=ObjectId("64bfe2e50123476789abcdef"),
            loan_name="Ипотека",
            opening_date=datetime(2020, 6, 12),
            amount=2000000,
            interest_rate=3.8,
            next_payment_date=datetime.now() + timedelta(days=30),
            monthly_payment=1200,
            debt=0,
            expiration_time=200,
            payments_overdue=0,
            co_borrowers=[],
            deposit=102
        ).save()
    ]

    credit_history = [
        CreditHistory(
            _id=ObjectId("64bfe2d10123456789abcdef"),
            loan_id=credits[0]._id,
            status="opened"
        ),
        CreditHistory(
            _id=ObjectId("64bfe2d20123456789abcdef"),
            loan_id=credits[1]._id,
            status="closed",
            closing_date=datetime(2024, 10, 1)
        ),
        CreditHistory(
            _id=ObjectId("64bfe2d30123456789abcdef"),
            loan_id=credits[2]._id,
            status="opened"
        ),
        CreditHistory(
            _id=ObjectId("64bfe2d40123456789abcdef"),
            loan_id=credits[3]._id,
            status="opened"
        ),
        CreditHistory(
            _id=ObjectId("64bfe2d50123456789abcdef"),
            loan_id=credits[4]._id,
            status="opened"
        )
    ]
    
    clients = [
        Client(_id=ObjectId("64bfe2d70123456789abcdef"),
               name="John Bobkov Alexandrovich",
               email="john@example.com",
               password="pass123",
               workplace='АО "Крутые котята"',
               post='Senior Python-Backend developer',
               birthdate='2003-12-12',
               marital_status="single",
               amount_of_children=0,
               salary=1000000,
               self_employment_status="self-employed",
               owned_property=[Property(type="Квартира", value="1200000", legal="Квартира 5 м^2 в центре Петербурга по адресу наб. реки Карповки, д. 7")],
               credit_history=[credit_history[0],credit_history[2],credit_history[3]],).save(),
        Client(_id=ObjectId("64bfe2d80123456789abcdef"),
               name="Jane Usacheva Vladimirovna",
               email="jane@example.com",
               password="pass123",
               workplace='ООО "Смешные яички"',
               salary=10000,
               amount_of_children=2,
               post='Менеджер по лопатам',
               self_employment_status="self-employed",
               marital_status="single",
               birthdate='2001-09-11',
               credit_history=[credit_history[1]]).save(),
        Client(_id=ObjectId("64bfe2d90123456789abcdef"),
               name="Alice Kamynina Bobkovna",
               email="alice@example.com",
               password="pass123",
               workplace='АО "Крутые котята"',
               salary=1000,
               amount_of_children=0,
               self_employment_status="self-employed",
               marital_status="single",
               post='Почтальон',
               owned_property=[Property(type="Квартира", value="200000", legal="Квартира 40 м^2 в центре Светлогорска по адресу ул. Калинина, д. 48")],
               birthdate='2003-10-15',
               credit_history=[credit_history[2]]).save()
    ]

    credit_requests = [
        CreditRequest(_id=ObjectId("64bfe2e60123456789abcdef"), client_id=clients[0]._id, loan_id=credits[0]._id, request_time=datetime(2024, 9, 1), status="approved").save(),
        CreditRequest(_id=ObjectId("64bfe2e70123456789abcdef"), client_id=clients[1]._id, loan_id=credits[1]._id, request_time=datetime(2023, 8, 12), status="processing").save(),
        CreditRequest(_id=ObjectId("64bfe2e60123956789abcdef"), client_id=clients[0]._id, loan_id=credits[2]._id, request_time=datetime(2022, 10, 15), status="approved").save(),
        CreditRequest(_id=ObjectId("64bfe2e90123456789abcdef"), client_id=clients[0]._id, loan_id=credits[3]._id, request_time=datetime(2021, 5, 1), status="approved").save(),
        CreditRequest(_id=ObjectId("64bfe2e11123456789abcdef"), client_id=clients[2]._id, loan_id=credits[4]._id, request_time=datetime(2020, 6, 12), status="rejected").save()
    ]
    
    interaction_history = [
        InteractionHistory(_id=ObjectId("64bfe2da0123456789abcdef"), credit_request_id=credit_requests[0]._id, decision=True, processing_date=datetime(2024, 9, 1)),
        InteractionHistory(_id=ObjectId("64bfe2dc0123456789abcdef"), credit_request_id=credit_requests[2]._id, decision=True, processing_date=datetime(2022, 10, 15)),
        InteractionHistory(_id=ObjectId("64bfe2de0123456789abcdef"), credit_request_id=credit_requests[3]._id, decision=True, processing_date=datetime(2021, 5, 1)),
        InteractionHistory(_id=ObjectId("64bfe2de0112456789abcdef"), credit_request_id=credit_requests[4]._id, decision=False, processing_date=datetime(2020, 6, 12))
    ]

    admins = [
        Admin(_id=ObjectId("64bfe2e00123456789abcdef"),
              name="Алексей Админов Админович",
              email="admin1@example.com",
              password="adminpass",
              post="Старший сотрудник",
              interaction_history=interaction_history).save(),
        Admin(_id=ObjectId("64bfe2e10123456789abcdef"),
              name="Admin2",
              email="admin2@example.com",
              password="adminpass",
              post="Младший сотрудник",
              interaction_history=[]).save(),
        Admin(_id=ObjectId("64bfe2e20123456789abcdef"),
              name="Admin3",
              email="admin3@example.com",
              password="adminpass",
              post= "Стажер",
              interaction_history=[]).save()
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
    return output_file
    
    
def load_data_from_json(dump_file):
    with open(dump_file, 'r') as f:
        data = json.load(f)
    for client_data in data.get("clients", []):
        Client(**client_data).save()
    for admin_data in data.get("admins", []):
        Admin(**admin_data).save()
    for credit_data in data.get("credits", []):
        Credit(**credit_data).save()
    for credit_request_data in data.get("credit_requests", []):
        CreditRequest(**credit_request_data).save()
    print("Данные успешно загружены из дампа.")

# create_sample_data()
# load_data_from_json(dump_data_to_json("mongo_dump.json"))
