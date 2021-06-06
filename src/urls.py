from django.urls import path, include

urlpatterns = [
    path("", include("src.budget.urls")),
    path("", include("src.habit_tracker.urls")),
    path("", include("src.purpose.urls")),
    path("todo/", include("src.todo.urls")),
]
