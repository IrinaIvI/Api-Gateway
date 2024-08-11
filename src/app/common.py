from datetime import datetime
from decimal import Decimal

import requests

TIMEOUT_MESSAGE = 'Превышено время ожидания'
ERROR_MESSAGE_PREFIX = 'Ошибка:'


def api_registration(login: str, password: str):
    """Отправляет запрос на регистрацию пользователя."""
    registration_params = {'login': login, 'password': password}
    return handle_request(
        url='http://host.docker.internal:8001/auth_service/registration',
        parameters=registration_params,
    )


def api_authorisation(login: str, password: str):
    """Отправляет запрос на авторизацию пользователя."""
    auth_params = {'login': login, 'password': password}
    return handle_request(
        url='http://host.docker.internal:8001/auth_service/authorisation',
        parameters=auth_params,
        request_type='post',
    )


def api_create_transaction(user_id: int, token: str, amount: Decimal, operation: str):
    """Отправляет запрос на создание транзакции."""
    actual_token = {'token': token}
    validation_response = handle_request(
        url='http://host.docker.internal:8001/auth_service/validate',
        parameters=actual_token,
    )
    if validation_response:
        transaction_params = {'user_id': user_id, 'amount': amount, 'operation': operation}
        return handle_request(
            url='http://host.docker.internal:8002/transaction_service/create_transaction',
            parameters=transaction_params,
            request_type='post',
        )
    return 'Invalid token'


def api_get_transaction(user_id: int, token: str, start: datetime, end: datetime):
    """Отправляет запрос на получение отчета о транзакциях."""
    actual_token = {'token': token}
    validation_response = handle_request(
        url='http://host.docker.internal:8001/auth_service/validate',
        parameters=actual_token,
    )
    if validation_response:
        transaction_report_params = {'user_id': user_id, 'start': start, 'end': end}
        return handle_request(
            url='http://host.docker.internal:8002/transaction_service/get_transaction',
            parameters=transaction_report_params,
        )
    return 'Invalid token'


def handle_request(url: str, parameters: dict, request_type: str = 'get'):
    """Отправляет HTTP-запрос и обрабатывает ответ."""
    try:
        response = requests.request(
            method=request_type,
            url=url,
            params=parameters,
            timeout=10,
        )
        response.raise_for_status()
        return response.json()
    except requests.Timeout:
        return TIMEOUT_MESSAGE
    except requests.RequestException as req_err:
        return f'{ERROR_MESSAGE_PREFIX} {req_err}'
