from rest_framework.routers import SimpleRouter

from . import views

app_name = "habit_tracker"

router = SimpleRouter()
router.register('habit', views.HabitViewSet, basename='habit')

urlpatterns = router.urls
