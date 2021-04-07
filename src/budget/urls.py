from rest_framework_extensions.routers import ExtendedSimpleRouter

from . import views

app_name = "budget"

extended_router = ExtendedSimpleRouter()

budget_board = extended_router.register(
    r"budget-board", views.BudgetBoardViewSet, basename="budget_board"
)
budget_board.register(
    r"transactions",
    views.TransactionViewSet,
    basename="transactions",
    parents_query_lookups=[views.TransactionViewSet.budget_board_lookup],
)
budget_board.register(
    r"categories",
    views.CategoryViewSet,
    basename="categories",
    parents_query_lookups=[views.CategoryViewSet.budget_board_lookup],
)

urlpatterns = extended_router.urls
