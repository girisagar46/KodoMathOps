from django.urls import path, include

urlpatterns = [
    path("users/", include("kodomath.users.urls")),
    path("mathops/", include("kodomath.mathops.urls")),
]
