from django.core.management.base import BaseCommand
from task_manager.models import Tasks
from account.models.users import User
from faker import Faker

fake = Faker(['en_US'])


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        users = User.objects.all()
        count_users = User.objects.count() +100
        usernames = []
        emails = []
        for i in range(User.objects.count()):
            usernames.append(users[i].username)
            emails.append(users[i].email)
        while User.objects.count() < count_users:
            username = fake.user_name()
            email = fake.email()
            if username not in usernames and email not in emails:
                usernames.append(username)
                emails.append(email)
                User.objects.create_user(username=username, email=email, password=username, is_staff=False, )






        self.style.SUCCESS('Successfully created tasks')

