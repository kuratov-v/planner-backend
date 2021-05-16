from django.db import models
from django.contrib.auth import get_user_model


class Project(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, editable=False)
    date_created = models.DateField(auto_now_add=True, editable=False)
    title = models.CharField(max_length=50)


class Section(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)


class Task(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    date_created = models.DateField(auto_now_add=True, editable=False)
    is_complete = models.BooleanField(default=False)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)

    class Meta:
        ordering = ["is_complete", "-date", "-id"]


class CheckList(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)


class Item(models.Model):
    check_list = models.ForeignKey(CheckList, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    is_complete = models.BooleanField(default=False)
