from rest_framework_extensions.routers import ExtendedSimpleRouter

from . import views

app_name = "todo"

extended_router = ExtendedSimpleRouter()

project = extended_router.register(
    r"projects", views.ProjectViewSet, basename="projects"
)

project.register(
    r"sections",
    views.SectionViewSet,
    basename="sections",
    parents_query_lookups=[views.SectionViewSet.project_lookup],
)

project.register(
    r"tasks",
    views.ProjectTaskViewSet,
    basename="project_tasks",
    parents_query_lookups=[views.ProjectTaskViewSet.project_lookup],
)

task = extended_router.register(r"tasks", views.TaskViewSet, basename="tasks")

check_list = task.register(
    r"check-list",
    views.CheckListViewSet,
    basename="check-list",
    parents_query_lookups=[views.CheckListViewSet.task_lookup],
)

check_list.register(
    r"items",
    views.ItemViewSet,
    basename="items",
    parents_query_lookups=[
        views.ItemViewSet.task_lookup,
        views.ItemViewSet.check_list_lookup,
    ],
)

urlpatterns = extended_router.urls
