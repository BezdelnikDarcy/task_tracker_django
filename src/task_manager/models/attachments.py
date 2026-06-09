from django.db import models

from config.models import BaseModel


class Attachments(BaseModel):
    name = models.CharField(
        max_length=64,
        unique=True,
        verbose_name="Наименование"
    )
    task = models.ForeignKey(
        to = "Tasks",
        related_name = "attachments",
        on_delete=models.CASCADE,
    )
    file = models.FileField(
        upload_to="attachments/files",
        blank=True,
        null=True,
        verbose_name="Файлы"
    )
    picture = models.FileField(
        upload_to='attachments/pictures',
        null=True,
        blank=True,
        verbose_name="Картинки",
    )


    class Meta:
        ordering = ('name',)
        db_table = 'attachments'
        verbose_name = 'Вложение'
        verbose_name_plural = 'Вложения'

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        if self.file:
            self.file.delete(save=False)
        if self.picture:
            self.picture.delete(save=False)

        super().delete(*args, **kwargs)
