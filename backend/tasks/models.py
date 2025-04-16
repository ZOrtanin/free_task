from django.db import models
from django.conf import settings
from django.utils import timezone


class TaskStatus(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_completed = models.BooleanField(default=False)
    deadline = models.DateTimeField(null=True, blank=True)

    status = models.ForeignKey(
        TaskStatus, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True)

    parent = models.ForeignKey(
        'self', 
        null=True, 
        blank=True, 
        on_delete=models.CASCADE, 
        related_name='children')

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tasks'
    )

    shared_with = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        blank=True, 
        related_name='shared_tasks')

    def get_breadcrumbs(self):
        task = self
        breadcrumbs = []
        while task.parent:
            breadcrumbs.insert(0, task.parent)
            task = task.parent
        return breadcrumbs

    def is_overdue(self):
        return self.deadline and self.deadline < timezone.now()

    def __str__(self):
        return self.title
