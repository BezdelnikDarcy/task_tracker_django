from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from src.config.models import BaseModel


class TaskStatus(models.TextChoices):
    CREATED = 'created'
    STARTED = 'started'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'
    FAILED = 'failed'

class Tasks(models.Model, BaseModel):
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
            MaxValueValidator(10)
        ],
        verbose_name="Приоритетность"
    )

    users = models.ManyToManyField(
        to = "User",
        related_name="tasks",

    )

    project = models.ForeignKey(
        to = "Project",
        on_delete=models.SET_NULL,
        related_name="tasks",
    )

    assignee = models.ForeignKey(
        to="Users",
        on_delete=models.SET_NULL,
        related_name="tasks",
    )

    class Meta:
        ordering = ('priority', 'created_at')
        db_table = 'tasks'
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return self.name