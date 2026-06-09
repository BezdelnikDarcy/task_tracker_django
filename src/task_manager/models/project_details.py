from django.db import models

from config.models import BaseModel


class ProjectDetails(BaseModel):
    info = models.CharField(
        max_length=64,
        unique=True,
        verbose_name="Информация"
    )
    serial_id = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="ID Проекта"
    )

    project = models.OneToOneField(
        to = "Projects",
        on_delete=models.CASCADE,
        related_name="project_detail",
    )

    class Meta:
        ordering = ('created_at',)
        db_table = 'projects_details'
        verbose_name = 'Детали проекта'
        verbose_name_plural = 'Детали проектов'

    def __str__(self):
        return self.info