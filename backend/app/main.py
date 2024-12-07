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

app = Flask(__name__)
app.config.from_object(Config)  # Загружаем конфигурацию из класса Config
CORS(app)

# Отключаем предыдущее соединение (если оно существует)
disconnect()

# Подключение к MongoDB с использованием MONGO_URI из конфигурации
connect(host=app.config['MONGO_URI'])

app.register_blueprint(auth_routes_bp)
app.register_blueprint(request_routes_bp)
app.register_blueprint(filter_routes_bp)
app.register_blueprint(profile_routes)
app.register_blueprint(statistic_routes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017/credit_database")