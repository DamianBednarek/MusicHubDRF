from django.urls import path
from .views import (
    ListTracksView,
    UploadTrackView,
    DeleteOneTrackView,
)


urlpatterns = [
    path("upload/", UploadTrackView.as_view(), name="upload-track"),
    path("list/", ListTracksView.as_view(), name="list-track"),
    path("delete/<str:pk>/", DeleteOneTrackView.as_view(), name="delete-track"),
]
