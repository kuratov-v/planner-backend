from rest_framework_extensions.routers import ExtendedSimpleRouter
from rest_framework.routers import SimpleRouter

from . import views

app_name = "todo"

extended_router = ExtendedSimpleRouter()
router = SimpleRouter()

project = extended_router.register(
    r"projects", views.ProjectViewSet, basename="projects"
)

task = extended_router.register(r"tasks", views.TaskViewSet, basename="tasks")

router.register(r"sections", views.SectionViewSet)
router.register(r"check-lists", views.CheckListViewSet)
router.register(r"items", views.ItemViewSet)

project.register(
    r"sections",
    views.SectionViewSetNested,
    basename="sections",
    parents_query_lookups=[views.SectionViewSetNested.project_lookup],
)

project.register(
    r"tasks",
    views.TaskViewSetNested,
    basename="project_tasks",
    parents_query_lookups=[views.TaskViewSetNested.project_lookup],
)

check_list = task.register(
    r"check-list",
    views.CheckListViewSetNested,
    basename="check-list",
    parents_query_lookups=[views.CheckListViewSetNested.task_lookup],
)

check_list.register(
    r"items",
    views.ItemViewSetNested,
    basename="items",
    parents_query_lookups=[
        views.ItemViewSetNested.task_lookup,
        views.ItemViewSetNested.check_list_lookup,
    ],
)

urlpatterns = extended_router.urls
urlpatterns += router.urls
