import io

import pytest
from PIL import Image
from faker import Faker
from rest_framework.test import APIClient

from MusicHub.users.test.user_factory import UserFactory

fake = Faker()


@pytest.fixture(scope="function")
def user_schema():
    return {
        "email": fake.email(),
        "password": "abcABC123*",
        "confirm_password": "abcABC123*",
        "first_name": fake.first_name(),
        "last_name": fake.last_name()
    }


@pytest.fixture(scope="function")
def user():
    return UserFactory.create()


@pytest.fixture(scope="function")
def client():
    return APIClient(format="json")


@pytest.fixture(scope="function")
def auth_client(client, user):
    client.force_authenticate(user=user)
    return client


@pytest.fixture(scope="function")
def mock_file(name="test.jpg", width=500, height=500, format="JPEG"):
    image = Image.new('RGB', (width, height))
    file_mock = io.BytesIO()
    file_mock.name = name
    image.save(file_mock, format=format)
    file_mock.seek(0)

    return file_mock
