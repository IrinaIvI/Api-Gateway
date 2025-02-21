from datetime import datetime
from decimal import Decimal
from typing import Dict, Any

import httpx
from fastapi import UploadFile, File

TIMEOUT_MESSAGE = 'Превышено время ожидания'
ERROR_MESSAGE_PREFIX = 'Ошибка:'
INVALID_TOKEN_MESSAGE = 'Токен недействителен'
POST_METHOD = 'POST'
HTTP_OK_STATUS = 200
DEFAULT_FILE = File(...)


async def api_registration(login: str, password: str) -> Dict[str, Any]:
    """Отправляет запрос на регистрацию пользователя."""
    registration_params = {'login': login, 'password': password}
    response = await handle_request(
        url='http://auth-service:8001/auth_service/registration',
        parameters=registration_params,
        request_type=POST_METHOD,
    )
    return response


async def api_authorisation(login: str, password: str):
    """Отправляет запрос на авторизацию пользователя."""
    auth_params = {'login': login, 'password': password}
    response = await handle_request(
        url='http://auth-service:8001/auth_service/authorisation',
        parameters=auth_params,
        request_type=POST_METHOD,
    )
    return response


async def api_create_transaction(user_id: int, token: str, amount: Decimal, operation: str):
    """Отправляет запрос на создание транзакции."""
    validation_response = await api_validate(user_id, token)
    if validation_response:
        transaction_params = {'user_id': user_id, 'amount': amount, 'operation': operation}
        response = await handle_request(
            url='http://transaction-service:8002/transaction_service/create_transaction',
            parameters=transaction_params,
            request_type=POST_METHOD,
        )
        return response
    return INVALID_TOKEN_MESSAGE


async def api_get_transaction(user_id: int, token: str, start: datetime, end: datetime):
    """Отправляет запрос на получение отчета о транзакциях."""
    validation_response = await api_validate(user_id, token)
    if validation_response:
        transaction_report_params = {'user_id': user_id, 'start': start, 'end': end}
        response = await handle_request(
            url='http://transaction-service:8002/transaction_service/get_transaction',
            parameters=transaction_report_params,
        )
        return response
    return INVALID_TOKEN_MESSAGE


async def api_validate(user_id: int, token: str):
    """Проверка действительность токена."""
    actual_token = {'user_id': user_id, 'token': token}
    response = await handle_request(
        url='http://auth-service:8001/auth_service/validate',
        parameters=actual_token,
    )
    return response.get('status') == HTTP_OK_STATUS


async def api_verify(user_id: int, token: str, img_path: UploadFile = DEFAULT_FILE):
    """Проверка действительности токена и верификация лица."""
    validation_response = await api_validate(user_id, token)
    if validation_response:
        file_content = await img_path.read()
        files = {'photo': (img_path.filename, file_content, img_path.content_type)}
        parameters = {'user_id': user_id}
        verify_response = await handle_request(
            url='http://auth-service:8001/auth_service/verify',
            parameters=parameters,
            files=files,
            request_type=POST_METHOD,
        )
        if isinstance(verify_response, httpx.Response):
            return verify_response
        return {'status': 'error', 'message': verify_response}
    return INVALID_TOKEN_MESSAGE


async def handle_request(url: str, parameters: dict = None, files: dict = None, request_type: str = 'get'):
    """Отправляет HTTP-запрос и обрабатывает ответ."""
    async with httpx.AsyncClient() as client:
        if request_type == POST_METHOD:
            response = await client.post(url, params=parameters, files=files, timeout=10)
        else:
            response = await client.get(url, params=parameters, timeout=10)
        return response.json()


async def auth_ready():
    """Проверяет состояние auth сервиса."""
    return await handle_request(url='http://auth-service:8001/auth_service/health/ready')


async def transaction_ready():
    """Проверяет состояние transaction сервиса."""
    return await handle_request(url='http://transaction-service:8002/transaction_service/health/ready')


async def face_verification_ready():
    """Проверяет состояние face verification сервиса."""
    return await handle_request(url='http://face-verification:8003/face_verification/health/ready')
