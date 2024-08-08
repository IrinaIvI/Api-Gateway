from app.common import api_authorisation, api_create_transaction, api_get_transaction, api_registration
from datetime import datetime
import pytest
import requests


test_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2xvZ2luIjoibWlrZSIsInBhc3N3b3JkIjoic3VwZXJib3NzIn0.qLj7Fh9Vr7bM9DE9s3Y_SPIrmApxlokn7Xb9DhAIE5s"
time = datetime.now()

@pytest.mark.parametrize('login, password', [
    pytest.param('mike', 'superboss', id='is correct'),
    pytest.param('', 'superboss', id='is not correct', marks=pytest.mark.xfail()),
    pytest.param('mike', '', id='is not correct', marks=pytest.mark.xfail()),
    pytest.param('', '', id='is not correct', marks=pytest.mark.xfail()),
])
def test_api_registration(login, password):
    result = api_registration(login, password)
    params={'login': login, 'password': password}
    response = requests.get(url="http://host.docker.internal:8001/auth_service/registration", params=params)
    assert result == response.json()

@pytest.mark.parametrize('login, password', [
    pytest.param('mike', 'superboss', id='is correct'),
    pytest.param('', 'superboss', id='is not correct', marks=pytest.mark.xfail()),
    pytest.param('mike', '', id='is not correct', marks=pytest.mark.xfail()),
    pytest.param('', '', id='is not correct', marks=pytest.mark.xfail()),
    pytest.param('johny', 'pwd123', id='is not correct', marks=pytest.mark.xfail()),
])
def test_api_authorisation(login, password):
    params={'login': login, 'password': password}
    response = requests.post(url='http://host.docker.internal:8001/auth_service/authorisation', params=params)
    result = api_authorisation(login, password)
    assert response.json() == result


@pytest.mark.parametrize('user_id, token, amount, transaction_type',
 [pytest.param(1, test_token, 1000, '+',  id='is correct'),
  pytest.param(4, test_token, 1000, '+', id='is not correct', marks=pytest.mark.xfail()),
  pytest.param(1, test_token, -1000, '+', id='is not correct', marks=pytest.mark.xfail()),
  pytest.param(1, test_token, 1000, '?', id='is not correct', marks=pytest.mark.xfail()),
  ]
)
def test_api_create_transaction(user_id, token, amount, transaction_type):
    requests.get(url="http://host.docker.internal:8002/transaction_service/router_create_base")
    api_registration('mike', 'superboss')
    api_authorisation('mike', 'superboss')
    result = api_create_transaction(user_id, token, amount, transaction_type)
    assert result == 'Correct operation'

@pytest.mark.parametrize('user_id, token, start, end', [
    pytest.param(2, test_token, time, time, id='is correct'),
    pytest.param(4, test_token, time, time, id='is not correct', marks=pytest.mark.xfail())
])
def test_get_transaction(user_id, token, start, end):
    requests.get(url="http://host.docker.internal:8002/transaction_service/router_create_base")
    api_create_transaction(2, token, 1500, '-')
    resulting_report = api_get_transaction(user_id, token, start, end)
    params={'user_id': user_id, 'start': start, 'end': end}
    report = requests.get(url='http://host.docker.internal:8002/transaction_service/get_transaction', params=params)
    assert resulting_report == report.json()

