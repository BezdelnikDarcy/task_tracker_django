from django.db import models

from config.models import BaseModel


class Comments(BaseModel):
    message = models.CharField(
        max_length=256,
        verbose_name="Текст комментария"
    )

    user = models.ForeignKey(
        to = "account.User",
        on_delete=models.SET_NULL,
        related_name="comments",
        null=True,
        blank=True,
    )
    task = models.ForeignKey(
        to = "Tasks",
        on_delete=models.CASCADE,
        related_name="comments",
    )



    class Meta:
        ordering = ['created_at', ]
        db_table = 'comments'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.message