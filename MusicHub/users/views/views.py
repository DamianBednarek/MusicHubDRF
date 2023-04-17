from rest_framework.authtoken.models import Token as SigninToken
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from social_core.exceptions import AuthForbidden
from social_django.utils import psa

from MusicHub.codes.models import ResetPasswordCode, SignUpCode
from ..models import User
from ..serializers import (
    ResetPasswordEmailSerializer,
    ResetPasswordSerializer,
    SignupSerializer,
    SocialAuthSerializer,
)
from ..user_service import (
    check_code_for_verification,
    reset_password_email,
)
from ...codes.helpers import get_or_400
from ...main.exception_handler import CustomUserException


class SignUpView(CreateAPIView):
    """
    View Responsible for creating a new user.
    """
    serializer_class = SignupSerializer


class SignUpVerifyView(APIView):
    """View responsible for confirming new user."""

    def get(self, request):
        code = get_or_400(SignUpCode, code=request.query_params.get("code"))
        code.user.is_verified = True
        code.user.save()
        code.delete()
        return Response(data="Registration complete", status=200)


class RecoverPassword(GenericAPIView, UpdateModelMixin):  # TODO refactor in the future
    """
    View to handle sending email with reset password link and
    changing password to a new one
    """

    http_method_names = ["post", "patch"]

    def get_queryset(self):
        if self.request.method == "POST":
            return User.objects.get_queryset_verified()
        elif self.request.method == "PATCH":
            code = self.request.query_params.get("code")
            return check_code_for_verification(code, ResetPasswordCode).user

    def get_serializer(self, *args, **kwargs):
        if self.request.method == "POST":
            return ResetPasswordEmailSerializer(*args, **kwargs)
        else:
            return ResetPasswordSerializer(*args, **kwargs)

    def get_object(self):
        return self.get_queryset()

    def post(self, request, *args, **kwargs):
        """
        Sends email with link to reset password for given email address
        """
        try:
            serializer = ResetPasswordEmailSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = self.get_queryset().get(email=request.data.get("email"))
            reset_password_email(user)
        except User.DoesNotExist:
            raise CustomUserException("Account with given email does not exists")
        return Response(
            status=200, data="Reset link was successfully send to given address email"
        )

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


@api_view(["POST"])
@psa()
def social_sign_google(request, backend):  # TODO Move this view to auth package
    """View to exchange google API token for application authorization token
    If no user is associated with Google token data, user will be created
    otherwise, user will be logged in
    """
    serializer = SocialAuthSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        try:
            user = request.backend.do_auth(request.data.get("access_token"))
        except AuthForbidden as e:
            raise CustomUserException(str(e))
        token, created = SigninToken.objects.get_or_create(user=user)

        return Response(status=200, data={"token": token.key})
