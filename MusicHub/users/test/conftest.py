import pytest
from faker import Faker
from rest_framework.test import APIClient

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
def client():
    return APIClient(format="json")
