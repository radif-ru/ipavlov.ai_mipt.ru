import pytest
from rest_framework.utils import json

from users.models import HospitalUser


@pytest.fixture
def user_data():
    return {'id': 1, 'email': 'test@local.com', 'username': 'user_name',
            'password': 'qwerty'}


@pytest.fixture
def login_data():
    return json.dumps({"username": "user_name", "password": "qwerty"})


@pytest.fixture
def create_test_user(user_data):
    user_model = HospitalUser
    test_user = user_model.objects.create_user(**user_data)
    test_user.set_password(user_data.get('password'))
    return test_user


@pytest.fixture
def authenticated_user(client, user_data):
    user_model = HospitalUser
    test_user = user_model.objects.create_user(**user_data)
    test_user.set_password(user_data.get('password'))
    test_user.save()
    client.login(**user_data)
    return test_user
