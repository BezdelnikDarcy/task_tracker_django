import random
from django.core.management.base import BaseCommand
from task_manager.models import Tasks, Comments
from account.models.users import User
from faker import Faker
fake = Faker(['en_US'])
class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        count = 0
        users = list(User.objects.all())
        tasks = list(Tasks.objects.all())
        messages = []
        for task in tasks:
            if count % 10000 == 0 and count != 0:
                Comments.objects.bulk_create(messages)
                messages = []
            count += 1
            comment = Comments(
                message=fake.text(max_nb_chars=50),
                task=task,
                user=random.choice(users),
            )
            messages.append(comment)
        Comments.objects.bulk_create(messages)