from app.common import (
    api_authorisation,
    api_create_transaction,
    api_get_transaction,
    api_registration,
)
from datetime import datetime
import pytest

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

time = datetime.now()

@pytest.mark.asyncio
@pytest.mark.parametrize('login, password', [
    pytest.param('mike', 'superboss', id='is correct'),
    pytest.param('', 'superboss', id='is not correct', marks=pytest.mark.xfail()),
    pytest.param('mike', '', id='is not correct', marks=pytest.mark.xfail()),
    pytest.param('', '', id='is not correct', marks=pytest.mark.xfail()),
])
async def test_api_registration(login, password):
    response = await api_registration(login, password)
    assert response['status'] == 200

# @pytest.mark.asyncio
# @pytest.mark.parametrize('login, password', [
#     pytest.param('mike', 'superboss', id='is correct'),
#     pytest.param('', 'superboss', id='is not correct', marks=pytest.mark.xfail()),
#     pytest.param('mike', '', id='is not correct', marks=pytest.mark.xfail()),
#     pytest.param('', '', id='is not correct', marks=pytest.mark.xfail()),
#     pytest.param('johny', 'pwd123', id='is not correct', marks=pytest.mark.xfail()),
# ])
# async def test_api_authorisation(login, password):
#     pass

# @pytest.mark.asyncio
# @pytest.mark.parametrize('user_id, token, amount, transaction_type',
#  [pytest.param(1, test_token, 1000, '+',  id='is correct'),
#   pytest.param(4, test_token, 1000, '+', id='is not correct', marks=pytest.mark.xfail()),
#   pytest.param(1, test_token, -1000, '+', id='is not correct', marks=pytest.mark.xfail()),
#   pytest.param(1, test_token, 1000, '?', id='is not correct', marks=pytest.mark.xfail()),
#   ]
# )
# async def test_api_create_transaction(user_id, token, amount, transaction_type):
#     pass

# @pytest.mark.asyncio
# @pytest.mark.parametrize('user_id, token, start, end', [
#     pytest.param(2, test_token, time, time, id='is correct'),
#     pytest.param(4, test_token, time, time, id='is not correct', marks=pytest.mark.xfail())
# ])
# async def test_get_transaction(user_id, token, start, end):
#     pass
