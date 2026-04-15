from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from config.models import BaseModel


class TaskStatus(models.TextChoices):
    CREATED = 'created'
    STARTED = 'started'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'
    FAILED = 'failed'

class Tasks(BaseModel):
    name = models.CharField(
        max_length=64,
        unique=True,
        verbose_name="Наименование"
    )
    description = models.TextField(
        null=True,
        verbose_name="Описание"
    )
    status = models.CharField(
        choices=TaskStatus,
        default=TaskStatus.CREATED,
        verbose_name="Статус"
    )
    is_reopened = models.BooleanField(
        default=False,
        verbose_name="Переоткрытие задачи"
    )
    priority = models.IntegerField(
        validators= [
            MinValueValidator(1),
            MaxValueValidator(5)
        ],
        verbose_name="Приоритетность"
    )

    project = models.ForeignKey(
        to = "Projects",
        on_delete=models.SET_NULL,
        related_name="tasks",
        null=True,
        blank=True,
        verbose_name="Проект"
    )

    assignee = models.ForeignKey(
        to="account.User",
        on_delete=models.SET_NULL,
        related_name="tasks",
        null=True,
        blank=True,
        verbose_name="Исполнитель"
    )

    class Meta:
        ordering = ('priority', '-created_at')
        db_table = 'tasks'
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return self.name

class ComplectedTasks(models.Manager):

    def get_queryset(self):
        return Tasks.objects.filter(status=TaskStatus.COMPLETED)


class EducationTasks(Tasks):

    class Meta:
        proxy = True

    objects = ComplectedTasks()