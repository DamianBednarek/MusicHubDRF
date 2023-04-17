from django.urls import path

from MusicHub.users.views.profile_view import (
    AddUpdateProfilePicture,
    ChangePassword,
    ProfileView,
)
from .views.views import (
    RecoverPassword,
    SignUpView,
    social_sign_google, SignUpVerifyView,
)

urlpatterns = [
    path("register/", SignUpView.as_view(), name="signup"),
    path("register/verify/", SignUpVerifyView.as_view(), name="signup-verify"),

    path("codes/google-sign/", social_sign_google, name="signin-google"),
    path("password-reset/", RecoverPassword.as_view(), name="reset-password"),

    path("me/", ProfileView.as_view(), name="profile"),
    path("me/profile-image/", AddUpdateProfilePicture.as_view(), name="upload-photo"),
    path("me/change-password/", ChangePassword.as_view(), name="change-password"),

]
