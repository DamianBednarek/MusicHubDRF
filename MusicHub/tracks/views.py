from rest_framework import generics, status
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from MusicHub.main.utils import LargeResultsSetPagination
from MusicHub.tracks.models import Track
from MusicHub.tracks.serializers import (
    AddTrackToPlaylistSerializer,
)
from MusicHub.tracks.serializers import CreateTrackSerializer, ListTrackSerializer


class UploadTrackView(CreateAPIView):
    """
    View for uploading new track by user
    """

    permission_classes = [IsAuthenticated]
    serializer_class = CreateTrackSerializer
    parser_classes = [MultiPartParser]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["user"] = self.request.user
        return context


class ListTracksView(generics.ListAPIView):
    """
    View for listing tracks owned by user
    """

    permission_classes = [IsAuthenticated]
    serializer_class = ListTrackSerializer
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        tracks = Track.objects.filter(created_by=self.request.user)
        return tracks.order_by("-created_at")


class DeleteOneTrackView(generics.DestroyAPIView):
    """
    View for deleting tracks owned by user
    provided id of track
    """

    permission_classes = [IsAuthenticated]
    serializer_class = ListTrackSerializer
    queryset = Track.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(
            {"detail": "Track deleted successfully!"},
            status=status.HTTP_204_NO_CONTENT,
        )


class AddTrackToPlaylist(UpdateAPIView):
    """View for adding user track to his playlist"""

    permission_classes = [IsAuthenticated]
    serializer_class = AddTrackToPlaylistSerializer
    http_method_names = ["patch"]

    def get_queryset(self):
        """Ensures that user can only add tracks that belong to him"""
        return Track.objects.filter(created_by=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["user"] = self.request.user
        return context
