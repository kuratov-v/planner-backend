from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework_extensions.mixins import NestedViewSetMixin

from .models import (
    Project,
    Task,
    CheckList,
    Item,
    Section,
)
from .serializers import (
    ProjectSerializer,
    ItemSerializer,
    SectionSerializer,
    CheckListSerializer,
    TaskSerializer,
    TaskReadSerializer,
)


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.validated_data["user"] = self.request.user
        return super(ProjectViewSet, self).perform_create(serializer)


class SectionViewSet(viewsets.ModelViewSet):
    serializer_class = SectionSerializer
    queryset = Section.objects.all()


class SectionViewSetNested(NestedViewSetMixin, SectionViewSet):
    project_lookup = "project_id"
    parent_lookup = f"parent_lookup_{project_lookup}"

    def get_queryset(self):
        return Section.objects.filter(project_id=self.kwargs[self.parent_lookup])


class TaskViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Task.objects.filter(section__project__user=self.request.user)

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return TaskReadSerializer
        return TaskSerializer


class TaskViewSetNested(NestedViewSetMixin, TaskViewSet):
    project_lookup = "project_id"
    parent_lookup = f"parent_lookup_{project_lookup}"

    def get_queryset(self):
        return Task.objects.filter(section__project_id=self.kwargs[self.parent_lookup])


class CheckListViewSet(viewsets.ModelViewSet):
    serializer_class = CheckListSerializer
    queryset = CheckList.objects.all()


class CheckListViewSetNested(NestedViewSetMixin, CheckListViewSet):
    task_lookup = "task_id"
    tasks_lookup = f"{task_lookup}__in"
    parent_lookup = f"parent_lookup_{task_lookup}"

    def get_queryset(self):
        return CheckList.objects.filter(task_id=self.kwargs[self.parent_lookup])


class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()


class ItemViewSetNested(NestedViewSetMixin, ItemViewSet):
    task_lookup = "check_list__task_id"
    check_list_lookup = "check_list_id"
    check_lists_lookup = f"{check_list_lookup}__in"
    parent_lookup = f"parent_lookup_{check_list_lookup}"

    def get_queryset(self):
        return Item.objects.filter(check_list_id=self.kwargs[self.parent_lookup])

    def perform_create(self, serializer):
        cl = CheckList.objects.get(id=self.kwargs[self.parent_lookup])
        serializer.validated_data["check_list"] = cl
        return super(ItemViewSetNested, self).perform_create(serializer)
