from django.contrib.auth.models import Group, Permission
from django.test import TestCase, Client
from task_manager.models.tasks import Tasks, TaskStatus
from account.models.users import User
from task_manager.models.comments import Comments
from task_manager.models.attachments import Attachments
from rest_framework import status
from rest_framework.test import APITestCase




class TestView(TestCase):
    def setUp(self):
        self.client = Client()
        test_user_email = 'test@test.com'
        test_password = 'test'

        self.user = User.objects._create_user(
            email=test_user_email,
            password=test_password
        )

        self.client.force_login(self.user)

        all_perms = Permission.objects.filter(content_type__app_label='task_manager')
        self.user.user_permissions.add(*all_perms) #Выдал все права для создания вложений, задач и т.д.

    def test_task_list(self):
        test_task_name = 'Test task'
        test_status = TaskStatus.CREATED
        test_priority = 2

        Tasks.objects.create(
            name=test_task_name,
            priority=test_priority,
            assignee=self.user,
            status=test_status,
        )
        path = '/tasks/'

        response = self.client.get(path=path)
        object = response.context['object_list']


        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(object), 1)
        self.assertEqual(object[0].name, test_task_name)
        self.assertEqual(object[0].priority, test_priority)
        self.assertEqual(object[0].status, test_status)
        self.assertEqual(object[0].assignee, self.user)

    def test_create_task_view(self):
        test_description = 'Test description'
        path = '/create_task'

        test_task_name = 'Test task'
        test_status = TaskStatus.CREATED
        test_priority = 2

        body = {
            "name": test_task_name,
            "description": test_description,
            "priority": test_priority,
            "status": test_status,
        }
        response = self.client.post(path=path, data=body)
        self.assertEqual(response.status_code, 302)

        tasks = Tasks.objects.all()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].name, test_task_name)
        self.assertEqual(tasks[0].priority, test_priority)
        self.assertEqual(tasks[0].status, test_status)
        self.assertEqual(tasks[0].description, test_description)

    def test_create_comment_form(self):
        test_comments = 'Test comments'
        test_user = self.user
        path = '/create_comment'

        test_task_name = 'Test task'
        test_status = TaskStatus.CREATED
        test_priority = 2

        test_task = Tasks.objects.create(
            name=test_task_name,
            priority=test_priority,
            assignee=self.user,
            status=test_status,
        )
        body = {
            "message": test_comments,
            "user": test_user.id,
            "task": test_task.id,
        }
        response = self.client.post(path=path, data=body)

        self.assertEqual(response.status_code, 302)

        comments = Comments.objects.all()
        self.assertEqual(len(comments), 1)
        self.assertEqual(comments[0].message, test_comments)
        self.assertEqual(comments[0].user, test_user)
        self.assertEqual(comments[0].task.name, test_task_name)

    def test_create_attachment_view(self):
        path = '/create_attachment'
        test_task_name = 'Test task'
        test_status = TaskStatus.CREATED
        test_priority = 2

        test_task = Tasks.objects.create(
            name=test_task_name,
            priority=test_priority,
            assignee=self.user,
            status=test_status,
        )
        name = "test attachment"
        body = {
            "name": name,
            "task": test_task.id,
        }

        response = self.client.post(path=path, data=body)

        self.assertEqual(response.status_code, 302)

        att = Attachments.objects.all()
        self.assertEqual(len(att), 1)
        self.assertEqual(att[0].name, name)
        self.assertEqual(att[0].task.name, test_task_name)



class TestApiView(APITestCase):
    def setUp(self):
        self.client = Client()
        test_user_email = 'test@test.com'
        test_password = 'test'
        self.user = User.objects._create_user(
            email=test_user_email,
            password=test_password
        )
        self.client.force_login(self.user)
        self.test_task_name = "test task"
        self.test_priority = 1
        Tasks.objects.create(
            name=self.test_task_name,
            priority=self.test_priority,
            assignee=self.user
        )

        gr = Group.objects.create(id=1)  # создаём группу с правами на добавление задачи
        add_task = [21, 25, 29, 33, 37, 41]
        gr.permissions.add(*add_task)
        self.user.groups.add(gr)  # даём права пользователю на создание задачи

    def test_create_api_task(self):
        path = "/api/tasks/"
        response = self.client.get(path)
        task = response.json()["results"][0]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(task["name"], self.test_task_name)
        self.assertEqual(task["priority"], self.test_priority)
        self.assertEqual(task["assignee"], self.user.id)
