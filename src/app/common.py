from datetime import datetime
from decimal import Decimal

import httpx

TIMEOUT_MESSAGE = 'Превышено время ожидания'
ERROR_MESSAGE_PREFIX = 'Ошибка:'


async def api_registration(login: str, password: str):
    """Отправляет запрос на регистрацию пользователя."""
    registration_params = {'login': login, 'password': password}
    return await handle_request(
        url='http://host.docker.internal:8001/auth_service/registration',
        parameters=registration_params,
    )


async def api_authorisation(login: str, password: str):
    """Отправляет запрос на авторизацию пользователя."""
    auth_params = {'login': login, 'password': password}
    return await handle_request(
        url='http://host.docker.internal:8001/auth_service/authorisation',
        parameters=auth_params,
        request_type='post',
    )


async def api_create_transaction(user_id: int, token: str, amount: Decimal, operation: str):
    """Отправляет запрос на создание транзакции."""
    actual_token = {'id': id, 'token': token}
    validation_response = await handle_request(
        url='http://host.docker.internal:8001/auth_service/validate',
        parameters=actual_token,
    )
    if validation_response:
        transaction_params = {'user_id': user_id, 'amount': amount, 'operation': operation}
        return await handle_request(
            url='http://host.docker.internal:8002/transaction_service/create_transaction',
            parameters=transaction_params,
            request_type='post',
        )
    return 'Invalid token'


async def api_get_transaction(user_id: int, token: str, start: datetime, end: datetime):
    """Отправляет запрос на получение отчета о транзакциях."""
    actual_token = {'id': id, 'token': token}
    validation_response = await handle_request(
        url='http://host.docker.internal:8001/auth_service/validate',
        parameters=actual_token,
    )
    if validation_response:
        transaction_report_params = {'user_id': user_id, 'start': start, 'end': end}
        return await handle_request(
            url='http://host.docker.internal:8002/transaction_service/get_transaction',
            parameters=transaction_report_params,
        )
    return 'Invalid token'


async def handle_request(url: str, parameters: dict = None, request_type: str = 'get'):
    """Отправляет HTTP-запрос и обрабатывает ответ."""
    async with httpx.AsyncClient() as client:
        try:
            if request_type == 'post':
                response = await client.post(url, params=parameters, timeout=10)
            else:
                response = await client.get(url, params=parameters, timeout=10)

            response.raise_for_status()
            return response.json()
        except httpx.TimeoutException:
            return TIMEOUT_MESSAGE
        except httpx.HTTPStatusError as http_err:
            return f'{ERROR_MESSAGE_PREFIX} {http_err}'
        except httpx.RequestError as req_err:
            return f'{ERROR_MESSAGE_PREFIX} {req_err}'
