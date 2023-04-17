import pytest

from MusicHub.codes.models import SignUpCode
from MusicHub.users.models import User
from MusicHub.users.test.user_factory import UserNotVerified


@pytest.mark.django_db
class TestSignUp:
    path = "/api/users/register/"

    def test_signup_success(self, client, user_schema):
        response = client.post(self.path, data=user_schema)

        assert response.status_code == 201
        assert User.objects.get(email=user_schema.get("email"))

    def test_email_taken(self, client, user_schema):
        client.post(self.path, data=user_schema)

        response = client.post(self.path, data=user_schema)

        assert response.status_code == 400
        assert "user with this email address already exists" in response.data.get("message")

    @pytest.mark.parametrize("email", ["test", "test@@example.com",
                                       "test.example.com", "test@example..com",
                                       "test@.com", "12345", "test@*&^$*.com",
                                       "", " "])
    def test_wrong_email(self, client, user_schema, email):
        user_schema["email"] = email

        response = client.post(self.path, data=user_schema)

        assert response.status_code == 400
        assert "Invalid: email" in response.data.get("message")

    @pytest.mark.parametrize("name", ["12345asda", "  ", "", "-", "test!@#$", "@$$%%%@#%",
                                      "a" * 21, " - - - -", "test12354"])
    def test_wrong_name(self, client, user_schema, name):
        user_schema["first_name"] = name

        response = client.post(self.path, data=user_schema)

        assert response.status_code == 400
        assert "Name not valid:" or "Invalid: first_name" in response.data.get("message")

    @pytest.mark.parametrize("password", ["", "  ", "1234567", "a" * 65, ""])
    def test_wrong_password(self, client, user_schema, password):
        user_schema["password"] = password

        response = client.post(self.path, data=user_schema)

        assert response.status_code == 400
        assert "Password not valid" or "Invalid: password" in response.data.get("message")

    def test_no_body(self, client):
        response = client.post(self.path)

        assert response.status_code == 400


@pytest.mark.django_db
class TestSignupVerify:
    path = "/api/users/register/verify/"

    def test_signup_verify_success(self, client):
        user = UserNotVerified.create()
        code = SignUpCode.objects.create(user)

        response = client.get(self.path, {"code": code.code})

        assert response.status_code == 200
        assert User.objects.get(email=user.email).is_verified
