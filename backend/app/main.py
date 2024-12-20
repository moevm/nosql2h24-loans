from flask import Flask
from flask_cors import CORS
from mongoengine import connect, disconnect
import os
from config import Config
from routes.auth_routes import bp as auth_routes_bp
from routes.request_routes import bp as request_routes_bp
from routes.filter import bp as filter_routes_bp
from routes.profile import bp as profile_routes
from routes.statistic import bp as statistic_routes
from routes.history import bp as history_routes
from models import Client
from pymongo import MongoClient
from utils.dump import create_sample_data

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

disconnect()
connect(host=app.config['MONGO_URI'])

@app.before_first_request
def check_collections():
    client = MongoClient(app.config['MONGO_URI'])
    db = client.get_default_database()
    collections = db.list_collection_names()
    if not collections:
        create_sample_data()

app.register_blueprint(auth_routes_bp)
app.register_blueprint(request_routes_bp)
app.register_blueprint(filter_routes_bp)
app.register_blueprint(profile_routes)
app.register_blueprint(statistic_routes)
app.register_blueprint(history_routes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)