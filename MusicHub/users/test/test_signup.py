import pytest

from MusicHub.users.models import User


@pytest.mark.django_db
class TestSignUp:
    path = "/api/users/registration/"

    def test_signup_success(self, client, user_schema):
        response = client.post(self.path, data=user_schema)

        assert response.status_code == 201
        assert User.objects.get(user_schema.get("email"))
