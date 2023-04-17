from django.conf import settings
from django.utils import timezone

from MusicHub.codes.models import ResetPasswordCode
from MusicHub.users.models import User
from ..emailProvider.service import send_email
from ..main.exception_handler import CustomUserException


def send_verification_email(user, signup_code):
    """Sent a verification email with link to the signed-up user"""

    error = send_email(
        subject="Verify email account: ",
        message=f"{settings.EMAIL_LINK_PATH}/api/user/signup/verify/?code={signup_code}",
        to_email=[user.email],
    )
    if error:
        raise CustomUserException(f"Email Server error: {error}\n"
                                  f"{settings.EMAIL_HOST_PASSWORD}")


def reset_password_email(user):
    """Sent a reset password email with link to the signed up user

    Args:
        user (User): User applying for password reset

    Raises:
        CustomUserException: Error when sending email
    """
    reset_code = ResetPasswordCode.objects.create(user)
    error = send_email(
        subject="Reset account password link: ",
        message=f"{settings.EMAIL_LINK_PATH}/api/user/reset-password/?code={reset_code}",
        to_email=[user.email],
    )
    if error:
        raise CustomUserException(error)


def has_token_expired(token):
    """Checks if token in links is not expired
    Returns:
        Boolean: True if token is expired, False otherwise
    """
    time = token.created_at + timezone.timedelta(hours=24)
    if time < timezone.now():
        return True
    return False


def check_code_for_verification(code, object_model):
    """
    Checks if verification code is valid ( not expired and not used)
    """
    try:
        verification_code = object_model.objects.get(code=code)
    except object_model.DoesNotExist:
        raise CustomUserException("Verification code is not a valid code")
    if has_token_expired(verification_code):
        raise CustomUserException("Token has expired.")

    return verification_code


def create_or_return_user(backend, response, *args, **kwargs):
    """Pipeline for social authentication
        responsible for creating new user or returning existing one

    Returns:
        User: created or pulled from database user
    """
    user, created = User.objects.get_or_create(
        email=response["sub"],
        first_name=response["given_name"],
        last_name=response["family_name"],
        password="",
        is_verified=True,
    )
    return user
