import pytest

from MusicHub.codes.models import ResetPasswordCode
from MusicHub.users.models import User


@pytest.mark.django_db
class TestRecoverPassword:
    path = "/api/users/password-reset/"

    def test_send_recover_link_success(self, client, user):
        response = client.post(self.path, data={"email": user.email})

        assert response.status_code == 200
        assert "Reset link was successfully send to given address email" in response.data

    def test_set_new_password(self, client, user):
        reset_code = ResetPasswordCode.objects.create(user).code
        data = {"password": "password1234",
                "confirm_password": "password1234"}

        response = client.patch(f"{self.path}?code={reset_code}", data=data)

        assert response.status_code == 200
        assert User.objects.get(email=user.email).check_password("password1234")
