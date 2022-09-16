from django.utils import timezone

from typing import List
from authemail.models import SignupCode, PasswordResetCode
from rest_framework.authtoken.models import Token as SigninToken
from .exception_handler import CustomUserException

from django.core.mail import send_mail

from MusicHub.config.settings import Common
from MusicHub.main.exception_handler import CustomUserException
from MusicHub.users.models import User


def send_email(subject: str, message: str, to_email: List[str]) -> None:
    """
    Send email from musichub email address to subject or list of subjects
    """
    send_mail(
        subject=subject,
        message=message,
        from_email=Common.EMAIL_FROM,
        recipient_list=to_email,
        fail_silently=False,
    )


def trim_spaces_from_data(data: str) -> str:
    """
    trim all whitespace characters from given string
    """
    for key, value in data.items():
        data[key] = " ".join(value.split())
    return data


def verification_email(user, request):
    ipaddr = request.META.get("REMOTE_ADDR", "0.0.0.0")
    signup_code = SignupCode.objects.create_signup_code(user, ipaddr)
    send_email(
        subject="Verify email account: ",
        message=f"http://localhost:8000/api/user/signup/verify/?code={signup_code}",
        to_email=[user.email],
    )


def reset_password_email(user, request):
    reset_code = PasswordResetCode.objects.create_password_reset_code(user)
    send_email(
        subject="Reset account password link: ",
        message=f"http://localhost:8000/api/user/reset-password/?code={reset_code}",
        to_email=[user.email],
    )


def check_code_for_verification(
    code: str, objectModel: SignupCode | PasswordResetCode
) -> str:
    try:
        verifiation_code = objectModel.objects.get(code=code)
    except objectModel.DoesNotExist:
        raise CustomUserException("Verification code is not a valid code")
    now = timezone.now()
    diff = now - verifiation_code.created_at

    if diff.days * 24 > 24:
        raise CustomUserException("Token has expired.")

    return verifiation_code


def check_sigin_code(code: str, objectModel: SigninToken) -> str:
    try:
        verification_code = objectModel.objects.get(key=code)
    except objectModel.DoesNotExist:
        raise CustomUserException("Verificaiton code is not a valid code.")
    now = timezone.now()
    diff = now - verification_code.created

    if diff.seconds // 60 > 60:
        raise CustomUserException("Token has expired.")

    return verification_code


def create_or_return_user(backend, response, *args, **kwargs):
    """Pipeline for social authentication
        responsible for creating new user or returning existing one

    Returns:
        User: created or pulled from database user
    """

    users = User.objects.filter(email=response["sub"])
    if users.exists():
        return users.get()
    else:
        user = User.objects.create_user(
            email=response["sub"],
            first_name=response["given_name"],
            last_name=response["family_name"],
            password="",
        )
        return user
