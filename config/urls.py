from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('rest_framework_social_oauth2.urls')),
    path("api/v1/", include("src.budget.urls")),
    path("api/v1/", include("src.account.urls")),
    path("api/v1/", include("src.habit_tracker.urls")),
    path("api/v1/", include("src.purpose.urls")),
]

