from mongoengine import (
    Document, EmbeddedDocument, StringField, EmailField, DateField, DateTimeField,
    FloatField, IntField, BooleanField, ListField, EmbeddedDocumentField, ObjectIdField,
    BinaryField
)
from datetime import datetime

class CreditHistory(EmbeddedDocument):
    _id = ObjectIdField(required=True)
    loan_id = ObjectIdField(required=True)
    status = StringField(choices=["opened", "expired", "closed"], required=True)
    closing_date = DateTimeField(default=datetime.utcnow())

class Client(Document):
    _id = ObjectIdField(required=True, primary_key=True)
    name = StringField(required=True)
    email = EmailField(required=True)
    workplace = StringField()
    sex = StringField()
    password = StringField(required=True)
    phone = StringField(max_length=11)
    age = IntField()
    birthdate = DateField()
    salary = FloatField()
    self_employment_status = StringField(choices=["self-employed", "entrepreneur", "idle"])
    owned_property = ListField(StringField(max_length=10))
    marital_status = StringField(choices=["married", "single"])
    spouse_workplace = StringField()
    spouse_salary = FloatField()
    amount_of_children = IntField()
    rating = FloatField()
    credit_history = ListField(EmbeddedDocumentField(CreditHistory))
    photo = BinaryField()

class InteractionHistory(EmbeddedDocument):
    _id = ObjectIdField(required=True)
    credit_request_id = ObjectIdField(required=True)
    processing_date = DateTimeField(default=datetime.utcnow())
    decision = BooleanField()

class Admin(Document):
    _id = ObjectIdField(required=True, primary_key=True)
    name = StringField(required=True)
    email = EmailField(required=True)
    sex = StringField()
    password = StringField(required=True)
    age = IntField()
    phone = StringField(max_length=10)
    post = StringField()
    birthdate = DateField()
    interaction_history = ListField(EmbeddedDocumentField(InteractionHistory))

class Credit(Document):
    _id = ObjectIdField(required=True, primary_key=True)
    loan_name = StringField(required=True)
    opening_date = DateTimeField(default=datetime.utcnow())
    expiration_time = IntField()
    amount = FloatField()
    interest_rate = FloatField()
    monthly_payment = FloatField()
    next_payment_date = DateField()
    debt = FloatField()
    payments_overdue = IntField()
    co_borrowers = ListField(StringField(max_length=750))
    deposit = FloatField()

class CreditRequest(Document):
    _id = ObjectIdField(required=True, primary_key=True)
    client_id = ObjectIdField(required=True)
    loan_id = ObjectIdField(required=True)
    request_time = DateTimeField(default=datetime.utcnow())
    status = StringField(choices=["processing", "approved", "rejected"], required=True)
