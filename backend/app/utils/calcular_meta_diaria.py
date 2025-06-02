from decimal import Decimal

def calcular_meta_diaria_recomendada(peso: float, idade: int) -> int:
    if peso is None or peso <= 5:
        raise ValueError("O peso do usuário deve ser um número positivo para o cálculo da meta.")

    if idade <= 17:
        ml_por_kg =  Decimal(40.0)
    elif 18 <= idade and idade <= 55:
        ml_por_kg =  Decimal(35.0)
    elif 55 <= idade and idade <= 65:
        ml_por_kg =  Decimal(30.0)
    else:
        ml_por_kg =  Decimal(25.0)      

    quantidade_ml = Decimal(peso) * ml_por_kg
    quantidade_ml = round(quantidade_ml)
    
    return quantidade_ml