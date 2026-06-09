import random
from django.core.management.base import BaseCommand
from task_manager.models import Projects
from account.models.users import User
from faker import Faker

fake = Faker(['en_US'])

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        projects = Projects.objects.all()
        users = User.objects.all()
        count_projects = Projects.objects.count() + 10
        project_names = []
        for i in range(Projects.objects.count()):
            project_names.append(projects[i].name)
        while Projects.objects.count() < count_projects:
            project_name = fake.text(max_nb_chars=60)
            if project_name not in project_names:
                project_names.append(project_name)
                Projects.objects.create(name=project_name, description=fake.text(max_nb_chars=40),
                                        owner=random.choice(users),
                                        )