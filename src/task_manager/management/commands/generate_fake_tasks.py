import random
from django.core.management.base import BaseCommand
from task_manager.models import Tasks, Projects
from account.models.users import User
from faker import Faker
from task_manager.models.tasks import TaskStatus
fake = Faker(['en_US'])
class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        count_tasks = Tasks.objects.count() + 1000000
        count = 0
        projects = Projects.objects.all()
        users = User.objects.all()
        while Tasks.objects.count() < count_tasks:
            tasks = []
            for i in range(10000):
                count += 1
                name_task = fake.text(max_nb_chars=50)
                task = Tasks(
                    name=f"Task {count} - {name_task}",
                    description=fake.text(max_nb_chars=64),
                    status=random.choice(TaskStatus),
                    priority=random.randint(1, 5),
                    project=random.choice(projects),
                    assignee=random.choice(users),
                )
                tasks.append(task)
            Tasks.objects.bulk_create(tasks)