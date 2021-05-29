from django.db import models
from django.contrib.auth import get_user_model


class Project(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        editable=False,
        related_name="projects",
    )
    date_created = models.DateField(auto_now_add=True, editable=False)
    title = models.CharField(max_length=50)
    is_hide_complete = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"


class Section(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="sections",
    )
    title = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Секция"
        verbose_name_plural = "Секции"


class Task(models.Model):
    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
        related_name="tasks",
    )
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    date_created = models.DateField(auto_now_add=True, editable=False)
    is_complete = models.BooleanField(default=False)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
        ordering = ["is_complete", "-date", "-id"]


class CheckList(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="check_lists",
    )
    title = models.CharField(max_length=50)
    is_hide_complete = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Чек-лист"
        verbose_name_plural = "Чек-листы"
        ordering = ["-id"]


class Item(models.Model):
    check_list = models.ForeignKey(
        CheckList,
        on_delete=models.CASCADE,
        related_name="items",
    )
    title = models.CharField(max_length=100)
    is_complete = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Пункт"
        verbose_name_plural = "Пункты"
        ordering = ["-id"]