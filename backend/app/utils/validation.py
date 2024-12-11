import re


def validate_phone_number(phone_number):
    # Регулярное выражение для валидации номера телефона
    phone_regex = re.compile(r'^(\+7|8)[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}$')
    return bool(phone_regex.match(phone_number))


def validate_passport_number(passport_number):
    passport_regex = re.compile(r'^\d{6}$')
    return bool(passport_regex.match(passport_number))


def validate_passport_series(passport_series):
    passport_regex = re.compile(r'^\d{4}$')
    return bool(passport_regex.match(passport_series))