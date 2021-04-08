from django.urls import path
from . import views


urlpatterns = [
    path("users/me/", views.UsersAPIView.as_view(), name="current-user-account"),
]
