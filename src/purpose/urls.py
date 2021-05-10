from rest_framework_extensions.routers import ExtendedSimpleRouter
from django.urls import path

from . import views

app_name = "purpose"

extended_router = ExtendedSimpleRouter()

purpose = extended_router.register(r"purpose", views.PurposeViewSet, basename="purpose")
purpose.register(
    r"results",
    views.PurposeResultViewSet,
    basename="purpose-results",
    parents_query_lookups=[views.PurposeResultViewSet.purpose_lookup],
)

urlpatterns = [
    path(
        "purpose/<int:id>/status/",
        views.PurposeStatusAPIView.as_view(),
        name="purpose-status",
    )
]
urlpatterns += extended_router.urls
