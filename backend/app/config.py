import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://db:27017/credit_database")
    # MONGO_URI = os.getenv("MONGO_URI", "mongodb://127.0.0.1:27017/credit_database")
