import pytest

from MusicHub.users.models import User


@pytest.mark.django_db
class TestProfileView:
    path = "/api/users/me/"

    def test_get_my_profile_success(self, auth_client, user):
        response = auth_client.get(self.path)

        assert response.status_code == 200
        assert response.data.get("email") == user.email

    def test_update_my_profile_success(self, auth_client, user):
        response = auth_client.patch(self.path, data={"first_name": "test", "last_name": "testowy"})

        assert response.status_code == 200
        assert User.objects.get(email=user.email).first_name == "test"
        assert User.objects.get(email=user.email).last_name == "testowy"

    def test_change_password_success(self, auth_client, user):
        data = {"old_password": "abcABC123*",
                "password": "password1234",
                "confirm_password": "password1234"}
        response = auth_client.patch(f"{self.path}change-password/", data=data)

        assert response.status_code == 200
        assert User.objects.get(email=user.email).check_password("password1234")

    def test_add_photo_success(self, auth_client, user, mock_file):
        response = auth_client.patch(f"{self.path}profile-image/",
                                     {"profile_avatar": mock_file}, format="multipart")

        assert response.status_code == 200
