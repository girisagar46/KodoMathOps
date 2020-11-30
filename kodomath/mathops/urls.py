from django.urls import path

from .views import PlayView

urlpatterns = [
    path("play/", PlayView.as_view(), name="play"),
]
