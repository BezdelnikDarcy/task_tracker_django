from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver

from task_manager.models import Tasks, Comments


@receiver(post_save, sender=Tasks)
def task_created(sender, instance, created, **kwargs):
    if created:
        instance.comments.create(
            message = "Task created",
            user = instance.assignee,
        )

