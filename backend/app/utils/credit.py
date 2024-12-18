from random import uniform

def generate_interest_rate(loan_name: str, loan_amount: float, expiration_time: int) -> float:
    interest_rate = 0
    expiration_time_to_rate = 0.13
    amount_to_rate = 2e-5
    
    if loan_name == "Молодежный кредит":
        min_rate = 1.0
        max_rate = 5.0
        amount_to_rate = 2e-5
    elif loan_name == "Ипотека":
        min_rate = 10.0
        max_rate = 25.0
        amount_to_rate = 3e-5
    elif loan_name == "Кредит наличными":
        min_rate = 10.0
        max_rate = 25.0
        amount_to_rate = 3e-5
    elif loan_name == "Автокредит":
        min_rate = 5.0
        max_rate = 10.0
        amount_to_rate = 2e-5
    elif loan_name == "Рефинансирование":
        min_rate = 1.0
        max_rate = 10.0
        amount_to_rate = 1e-5
    elif loan_name == "Кредитная карта":
        min_rate = 1.0
        max_rate = 2.0
        amount_to_rate = 2e-5
    else:
        min_rate = 9.0
        max_rate = 15.0
        
    interest_rate = max_rate - loan_amount * amount_to_rate
    interest_rate = max_rate - expiration_time * expiration_time_to_rate
    interest_rate = max(interest_rate, min_rate)
    
    return interest_rate