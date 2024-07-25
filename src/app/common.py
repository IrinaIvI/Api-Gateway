from decimal import Decimal
from datetime import datetime
import requests
from fastapi import Response

def api_registration(login: str, password: str):
    t_resp = requests.request(
        method="GET",
        url='http://127.0.0.1:8000//auth_service/registration',)

    response = Response(content=t_resp.contents, status_code=t_resp.status_code)
    return response

def api_authorisation(login: str, password: str):
    pass

def api_create_transaction(user_id: int, amount: Decimal, operation: str):
    pass

def api_get_transaction(user_id: int, start: datetime, end: datetime):
    pass
