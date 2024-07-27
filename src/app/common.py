from decimal import Decimal
from datetime import datetime
import requests


def api_registration(login: str, password: str):
    params={'login': login, 'password': password}
    response = requests.get(url="http://host.docker.internal:8001/auth_service/registration", params=params)
    return response.json()

def api_authorisation(login: str, password: str):
    params={'login': login, 'password': password}
    response = requests.post(url='http://host.docker.internal:8001/auth_service/authorisation', params=params)
    return response.json()

def api_create_transaction(user_id: int, token: str, amount: Decimal, operation: str):
    actual_token = {'token': token}
    response = requests.get(url='http://host.docker.internal:8001/auth_service/validate', params=actual_token)
    if response:
        params={'user_id': user_id, 'amount': amount, 'operation': operation}
        response = requests.post(url='http://host.docker.internal:8002/transaction_service/create_transaction', params=params)
        return response.json()
    else:
        return 'Invalid token'

def api_get_transaction(user_id: int, token: str, start: datetime, end: datetime):
    actual_token = {'token': token}
    response = requests.get(url='http://host.docker.internal:8001/auth_service/validate', params=actual_token)
    if response:
        params={'user_id': user_id, 'start': start, 'end': end}
        response = requests.get(url='http://host.docker.internal:8002/transaction_service/get_transaction', params=params)
        return response.json()
    else:
        return 'Invalid token'
