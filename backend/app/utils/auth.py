from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from flask import current_app, request
from functools import wraps

# Хеширование пароля
def hash_password(password):
    return generate_password_hash(password)

# Проверка пароля
def verify_password(password, hashed_password):
    return check_password_hash(hashed_password, password)

# Генерация JWT токена
def generate_token(user_id, expires_in=600):
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(seconds=expires_in)
    }
    return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")

# Проверка JWT токена
def verify_token(token):
    try:
        payload = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        return None  # Токен истек
    except jwt.InvalidTokenError:
        return None  # Невалидный токен

# Декоратор для защиты маршрутов
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return {"message": "Токен не найден"}, 401
        user_id = verify_token(token)
        if not user_id:
            return {"message": "Неверный или истекший токен"}, 401
        return f(user_id=user_id, *args, **kwargs)
    return decorated_function
