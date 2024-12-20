from mongoengine import (
    Document,
    EmbeddedDocument,
    StringField,
    EmailField,
    DateField,
    DateTimeField,
    FloatField,
    IntField,
    BooleanField,
    ListField,
    EmbeddedDocumentField,
    ObjectIdField,
    BinaryField,
)
from datetime import datetime


class CreditHistory(EmbeddedDocument):
    _id = ObjectIdField(required=True)
    loan_id = ObjectIdField(required=True)
    status = StringField(choices=["opened", "expired", "closed"], required=True)
    closing_date = DateTimeField(default=datetime.utcnow())


class Coborrowers(EmbeddedDocument):
    name = StringField(required=True)
    workplace = StringField(required=True)
    post = StringField(required=True)
    passport_series = StringField(min_length=4, max_length=4)
    passport_number = StringField(min_length=6, max_length=6)
    phone = StringField(max_length=20)

    def to_dict(self):
        return {
            "name": self.name,
            "workplace": self.workplace,
            "post": self.post,
            "passport_series": self.passport_series,
            "passport_number": self.passport_number,
            "phone": self.phone,
        }


class Property(EmbeddedDocument):
    type = StringField(required=True)
    value = FloatField(required=True)
    legal = StringField(required=True)

    def to_dict(self):
        return {"type": self.type, "value": self.value, "legal": self.legal}


class Client(Document):
    _id = ObjectIdField(required=True, primary_key=True)
    name = StringField(required=True)
    email = EmailField(required=True)
    workplace = StringField(default="")
    post = StringField()
    sex = StringField()
    password = StringField(required=True)
    phone = StringField(max_length=20)
    age = IntField()
    birthdate = DateField()
    salary = FloatField()
    passport_series = StringField(min_length=4, max_length=4)
    passport_number = StringField(min_length=6, max_length=6)
    self_employment_status = StringField(
        choices=["self-employed", "entrepreneur", "idle"]
    )
    owned_property = ListField(EmbeddedDocumentField(Property))
    marital_status = StringField(choices=["married", "single"])
    spouse_workplace = StringField(default="")
    spouse_salary = FloatField()
    spouse_post = StringField()
    amount_of_children = IntField()
    rating = FloatField(min_value=0.0, max_value=10.0, default=10.0)
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
    phone = StringField(max_length=20)
    post = StringField()
    birthdate = DateField()
    passport_series = StringField(min_length=4, max_length=4)
    passport_number = StringField(min_length=6, max_length=6)
    interaction_history = ListField(EmbeddedDocumentField(InteractionHistory))


class Credit(Document):
    _id = ObjectIdField(required=True, primary_key=True)
    loan_name = StringField(required=True)
    opening_date = DateTimeField(default=datetime.utcnow())
    expiration_time = IntField()
    amount = FloatField()
    interest_rate = FloatField()
    monthly_payment = FloatField()
    next_payment_date = DateField(default=datetime.utcnow())
    debt = FloatField()
    payments_overdue = IntField()
    co_borrowers = ListField(EmbeddedDocumentField(Coborrowers))
    deposit = FloatField()


class CreditRequest(Document):
    _id = ObjectIdField(required=True, primary_key=True)
    client_id = ObjectIdField(required=True)
    loan_id = ObjectIdField(required=True)
    request_time = DateTimeField(default=datetime.utcnow())
    status = StringField(choices=["processing", "approved", "rejected"], required=True)
