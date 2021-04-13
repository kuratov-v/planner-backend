from rest_framework_extensions.routers import ExtendedSimpleRouter

from . import views

app_name = "purpose"

extended_router = ExtendedSimpleRouter()

purpose = extended_router.register(r"purpose", views.PurposeViewSet, basename="purpose")
purpose.register(
    r"status",
    views.PurposeStatusViewSet,
    basename="purpose-status",
    parents_query_lookups=[views.PurposeStatusViewSet.purpose_lookup],
)
purpose.register(
    r"results",
    views.PurposeResultViewSet,
    basename="categories",
    parents_query_lookups=[views.PurposeResultViewSet.purpose_lookup],
)

urlpatterns = extended_router.urls
