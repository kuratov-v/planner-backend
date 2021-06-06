from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import token_verify

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/login/", include("rest_social_auth.urls_jwt_pair")),
    path("api/v1/token-verify/", token_verify),
    path("api/v1/", include("src.urls")),
]
