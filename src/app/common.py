from datetime import datetime
from decimal import Decimal

import httpx
from fastapi import UploadFile, File, HTTPException

TIMEOUT_MESSAGE = 'Превышено время ожидания'
ERROR_MESSAGE_PREFIX = 'Ошибка:'
INVALID_TOKEN_MESSAGE = 'Токен недействителен'
POST_METHOD = 'post'
HTTP_OK_STATUS = 200
DEFAULT_FILE = File(...)


async def api_registration(login: str, password: str):
    """Отправляет запрос на регистрацию пользователя."""
    registration_params = {'login': login, 'password': password}
    try:
        return await handle_request(
            url='http://host.docker.internal:8001/auth_service/registration',
            parameters=registration_params,
            request_type=POST_METHOD,
        )
    except HTTPException as http_exception:
        raise HTTPException(status_code=http_exception.status_code, detail=f'Ошибка регистрации: {http_exception.detail}')


async def api_authorisation(login: str, password: str):
    """Отправляет запрос на авторизацию пользователя."""
    auth_params = {'login': login, 'password': password}
    return await handle_request(
        url='http://host.docker.internal:8001/auth_service/authorisation',
        parameters=auth_params,
        request_type=POST_METHOD,
    )


async def api_create_transaction(user_id: int, token: str, amount: Decimal, operation: str):
    """Отправляет запрос на создание транзакции."""
    validation_response = await api_validate(user_id, token)
    if validation_response:
        transaction_params = {'user_id': user_id, 'amount': amount, 'operation': operation}
        return await handle_request(
            url='http://host.docker.internal:8002/transaction_service/create_transaction',
            parameters=transaction_params,
            request_type=POST_METHOD,
        )
    return INVALID_TOKEN_MESSAGE


async def api_get_transaction(user_id: int, token: str, start: datetime, end: datetime):
    """Отправляет запрос на получение отчета о транзакциях."""
    validation_response = await api_validate(user_id, token)
    if validation_response:
        transaction_report_params = {'user_id': user_id, 'start': start, 'end': end}
        return await handle_request(
            url='http://host.docker.internal:8002/transaction_service/get_transaction',
            parameters=transaction_report_params,
        )
    return INVALID_TOKEN_MESSAGE


async def api_validate(user_id: int, token: str):
    """Проверка действительность токена."""
    actual_token = {'user_id': user_id, 'token': token}
    response = await handle_request(
        url='http://host.docker.internal:8001/auth_service/validate',
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
            url='http://host.docker.internal:8001/auth_service/verify',
            parameters=parameters,
            files=files,
            request_type=POST_METHOD,
        )
        if isinstance(verify_response, httpx.Response):
            return verify_response
        return {'status': 'error', 'message': verify_response}
    return {'status': 'invalid', 'message': 'Invalid token'}


async def handle_request(url: str, parameters: dict = None, files: dict = None, request_type: str = 'get'):
    """Отправляет HTTP-запрос и обрабатывает ответ."""
    async with httpx.AsyncClient() as client:
        try:
            if request_type == POST_METHOD:
                response = await client.post(url, params=parameters, files=files, timeout=10)
            else:
                response = await client.get(url, params=parameters, timeout=10)

            response.raise_for_status()
            return response.json()
        except httpx.TimeoutException:
            return {'status_code': 408, 'detail': 'Request Timeout'}
        except httpx.HTTPStatusError as http_error:
            return {'status_code': http_error.response.status_code, 'detail': str(http_error)}
        except httpx.RequestError as request_error:
            return {'status_code': 500, 'detail': f'Request Error: {str(request_error)}'}


async def auth_ready():
    """Проверяет состояние auth сервиса."""
    return await handle_request(url='http://host.docker.internal:8001/auth_service/health/ready')


async def transaction_ready():
    """Проверяет состояние transaction сервиса."""
    return await handle_request(url='http://host.docker.internal:8002/transaction_service/health/ready')


async def face_verification_ready():
    """Проверяет состояние face verification сервиса."""
    return await handle_request(url='http://host.docker.internal:8003/face_verification/health/ready')
