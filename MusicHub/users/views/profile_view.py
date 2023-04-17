from rest_framework.generics import RetrieveUpdateAPIView, UpdateAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated

from MusicHub.users.serializers import (
    AddChangePictureSerializer,
    ChangePasswordSerializer,
    ProfileSerializer,
)


class ProfileView(RetrieveUpdateAPIView):
    """
     Get or update profile information
    """
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = None
    http_method_names = ["get", "patch"]

    def get_queryset(self):
        return self.request.user

    def get_object(self):
        return self.get_queryset()


class ChangePassword(UpdateAPIView):
    """
    View allowing authorized user to change their password
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer
    http_method_names = ["patch"]

    def get_queryset(self):
        return self.request.user

    def get_object(self):
        return self.get_queryset()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["user"] = self.request.user
        return context


class AddUpdateProfilePicture(UpdateAPIView):
    """
    View responsible for adding or updating existing user profile picture.
    User must be authenticated in order to add or update picture.
    default relative path to picture is /media/users/avatar/example.jpg

    """

    permission_classes = [IsAuthenticated]
    serializer_class = AddChangePictureSerializer
    parser_classes = [MultiPartParser]
    http_method_names = ["patch"]

    def get_queryset(self):
        return self.request.user

    def get_object(self):
        return self.get_queryset()
