from flask import Flask
from flask_cors import CORS
from mongoengine import connect
# from routes import auth_routes_bp
# from routes import request_routes_bp
from routes.auth_routes import bp as auth_routes_bp

app = Flask(__name__)
CORS(app)

# Подключение к MongoDB
connect('database_name')

# Регистрация маршрутов
# app.register_blueprint(auth_routes_bp)
# app.register_blueprint(request_routes_bp)
app.register_blueprint(auth_routes_bp)

if __name__ == '__main__':
    app.run(debug=True)