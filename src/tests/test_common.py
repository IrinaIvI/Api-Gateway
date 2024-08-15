from app.common import (
    api_authorisation,
    api_create_transaction,
    api_get_transaction,
    api_registration,
    api_validate,
    api_verify
)
from datetime import datetime
import pytest
from pytest_mock import MockerFixture
from fastapi import UploadFile
from io import BytesIO
import httpx

@pytest.fixture
async def user():
    """Фикстура для создания тестового пользователя."""
    login = 'mike'
    password = 'superboss'
    await api_registration(login, password)
    return login, password

@pytest.fixture
async def test_token(user):
    """Фикстура для получения токена пользователя."""
    login, password = user
    token = await api_authorisation(login, password)
    return token

@pytest.fixture
def mock_file():
    """Фикстура для корректного загруженного файла."""
    return UploadFile(filename="test.jpg", file=BytesIO(b'Valid image'))


time = datetime.now()

@pytest.mark.asyncio
@pytest.mark.parametrize('login, password', [
    pytest.param('mike', 'superboss', id='is correct'),
    pytest.param('', 'superboss', id='is not correct', marks=pytest.mark.xfail()),
    pytest.param('mike', '', id='is not correct', marks=pytest.mark.xfail()),
    pytest.param('', '', id='is not correct', marks=pytest.mark.xfail()),
])
async def test_api_registration(login, password, mocker: MockerFixture):
    mock_response = mocker.Mock(spec=httpx.Response)
    mock_response.json.return_value = {'status': 'success'}
    mocker.patch('app.common.handle_request', return_value=mock_response)
    response = await api_registration(login, password)
    assert response == {'status': 'success'}

@pytest.mark.asyncio
@pytest.mark.parametrize('login, password', [
    pytest.param('mike', 'superboss', id='is correct'),
    pytest.param('', 'superboss', id='is not correct', marks=pytest.mark.xfail()),
    pytest.param('mike', '', id='is not correct', marks=pytest.mark.xfail()),
    pytest.param('', '', id='is not correct', marks=pytest.mark.xfail()),
    pytest.param('johny', 'pwd123', id='is not correct', marks=pytest.mark.xfail()),
])
async def test_api_authorisation(login, password, mocker: MockerFixture):
    mock_response = mocker.Mock(spec=httpx.Response)
    mock_response.json.return_value = {'token': 'some_token'}
    mocker.patch('app.common.handle_request', return_value=mock_response)
    response = await api_authorisation(login, password)
    assert response == {'token': 'some_token'}

@pytest.mark.asyncio
@pytest.mark.parametrize('user_id, token, amount, transaction_type',
 [pytest.param(1, test_token, 1000, '+',  id='is correct'),
  pytest.param(4, test_token, 1000, '+', id='is not correct', marks=pytest.mark.xfail()),
  pytest.param(1, test_token, -1000, '+', id='is not correct', marks=pytest.mark.xfail()),
  pytest.param(1, test_token, 1000, '?', id='is not correct', marks=pytest.mark.xfail()),
  ]
)
async def test_api_create_transaction(user_id, token, amount, transaction_type, mocker: MockerFixture):
    mocker.patch('app.common.api_validate', return_value=True)
    mock_response = mocker.Mock(spec=httpx.Response)
    mock_response.json.return_value = {'status': 'Correct operation'}
    mocker.patch('app.common.handle_request', return_value=mock_response)
    response = await api_create_transaction(user_id, token, amount, transaction_type)
    assert response == {'status': 'Correct operation'}

@pytest.mark.asyncio
@pytest.mark.parametrize('user_id, token, start, end', [
    pytest.param(2, test_token, time, time, id='is correct'),
    pytest.param(4, test_token, time, time, id='is not correct', marks=pytest.mark.xfail())
])
async def test_get_transaction(user_id, token, start, end, mocker: MockerFixture):
    mocker.patch('app.common.api_validate', return_value=True)
    mock_response = mocker.Mock(spec=httpx.Response)
    mock_response.json.return_value = {'transactions': []}
    mocker.patch('app.common.handle_request', return_value=mock_response)
    response = await api_get_transaction(user_id, token, start, end)
    assert response == {'transactions': []}

@pytest.mark.asyncio
@pytest.mark.parametrize('token', [
    pytest.param(test_token, id='is correct'),
    pytest.param('invalid_token', id='is not correct', marks=pytest.mark.xfail())
])
async def test_validate(token, mocker: MockerFixture):
    mock_response = mocker.Mock(spec=httpx.Response)
    mock_response.status_code = 200
    mocker.patch('app.common.handle_request', return_value=mock_response)
    response = await api_validate(token)
    assert response is True


@pytest.mark.asyncio
@pytest.mark.parametrize('user_id, token', [
    pytest.param(1, 'valid_token', id='is correct'),
    pytest.param(1, 'invalid_token', id='is not correct', marks=pytest.mark.xfail())
])
async def test_verify(user_id, token, mock_file, mocker: MockerFixture):
    mocker.patch('app.common.api_validate', return_value=(token == 'valid_token'))
    mock_response = mocker.Mock(spec=httpx.Response)
    mock_response.json.return_value = {'status': 'verification successful'}
    mocker.patch('app.common.handle_request', return_value=mock_response)
    response = await api_verify(user_id, token, mock_file)
    assert response == {'status': 'verification successful'}
