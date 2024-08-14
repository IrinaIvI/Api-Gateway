from datetime import datetime
from decimal import Decimal
from fastapi import UploadFile, File

import httpx

TIMEOUT_MESSAGE = 'Превышено время ожидания'
ERROR_MESSAGE_PREFIX = 'Ошибка:'
INVALID_TOKEN = 'Токен недействителен'


async def api_registration(login: str, password: str):
    """Отправляет запрос на регистрацию пользователя."""
    registration_params = {'login': login, 'password': password}
    response =  await handle_request(
        url='http://host.docker.internal:8001/auth_service/registration',
        parameters=registration_params,
    )
    return response.json()

async def api_authorisation(login: str, password: str):
    """Отправляет запрос на авторизацию пользователя."""
    auth_params = {'login': login, 'password': password}
    response =  await handle_request(
        url='http://host.docker.internal:8001/auth_service/authorisation',
        parameters=auth_params,
        request_type='post',
    )
    return response.json()


async def api_create_transaction(user_id: int, token: str, amount: Decimal, operation: str):
    """Отправляет запрос на создание транзакции."""
    validation_response = await api_validate(token)
    if validation_response:
        transaction_params = {'user_id': user_id, 'amount': amount, 'operation': operation}
        response = await handle_request(
            url='http://host.docker.internal:8002/transaction_service/create_transaction',
            parameters=transaction_params,
            request_type='post',
        )
        return response.json()
    return INVALID_TOKEN


async def api_get_transaction(user_id: int, token: str, start: datetime, end: datetime):
    """Отправляет запрос на получение отчета о транзакциях."""
    validation_response = await api_validate(token)
    if validation_response:
        transaction_report_params = {'user_id': user_id, 'start': start, 'end': end}
        response = await handle_request(
            url='http://host.docker.internal:8002/transaction_service/get_transaction',
            parameters=transaction_report_params,
        )
        return response.json()
    return INVALID_TOKEN

async def api_validate(token: str) -> bool:
    """Проверка действительность токена."""
    actual_token = {'token': token}
    validation_response = await handle_request(
        url='http://host.docker.internal:8001/auth_service/validate',
        parameters=actual_token,
    )
    if isinstance(validation_response, httpx.Response):
        return validation_response.status_code == 200
    else:
        # Логика обработки ошибки, если response - строка ошибки
        print(validation_response)  # Логгирование ошибки
        return False


async def api_verify(user_id: int, token: str, img_path: UploadFile = File(...)):
    """Проверка действительности токена и верификация лица."""
    # Проверка JWT-токена
    validation_response = await api_validate(token)
    if validation_response:
        file_content = await img_path.read()
        files = {'photo': (img_path.filename, file_content, img_path.content_type)}
        parameters = {'user_id': user_id}
        verify_response = await handle_request(
        url='http://host.docker.internal:8001/auth_service/verify',
        parameters=parameters,
        files=files,
        request_type = 'post'
    )
        if isinstance(verify_response, httpx.Response):
            return verify_response.json()
        else:
            # Логика обработки ошибки
            return {'status': 'error', 'message': verify_response}
    return {'status': 'invalid', 'message': 'Invalid token'}


async def handle_request(url: str, parameters: dict = None, files: dict = None, request_type: str = 'get'):
    """Отправляет HTTP-запрос и обрабатывает ответ."""
    async with httpx.AsyncClient() as client:
        try:
            if request_type == 'post':
                response = await client.post(url, params=parameters, files=files, timeout=10)
            else:
                response = await client.get(url, params=parameters, timeout=10)

            response.raise_for_status()
            return response
        except httpx.TimeoutException:
            return TIMEOUT_MESSAGE
        except httpx.HTTPStatusError as http_err:
            return f'{ERROR_MESSAGE_PREFIX} {http_err}'
        except httpx.RequestError as req_err:
            return f'{ERROR_MESSAGE_PREFIX} {req_err}'


async def auth_ready():
    """Проверяет состояние auth сервиса."""
    return await handle_request(url='http://host.docker.internal:8001/auth_service/health/ready')


async def transaction_ready():
    """Проверяет состояние transaction сервиса."""
    return await handle_request(url='http://host.docker.internal:8002/transaction_service/health/ready')


async def face_verification_ready():
    """Проверяет состояние transaction сервиса."""
    return await handle_request(url='http://host.docker.internal:8003/face_verification/health/ready')
