from django.test import TestCase
from task_manager.models.forms import TaskForm, CommentForm
from task_manager.models.tasks import TaskStatus
from account.models.users import User
from task_manager.models.tasks import Tasks


class TestForms(TestCase):
    def setUp(self):
        self.user = User.objects._create_user(
            email='test@test.com',
            password='test'
        )
        self.task = Tasks.objects.create(
            name='Test Task',
            priority=2,
            assignee=self.user,
            status=TaskStatus.CREATED
        )

    def test_task_form_valid(self):
        form_data = {
            'name': 'New Task',
            'description': 'Description',
            'priority': 3,
            'status': TaskStatus.CREATED,
        }
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_task_form_invalid_high_priority_no_description(self):
        form_data = {
            'name': 'New Task',
            'description': '',
            'priority': 5,
            'status': TaskStatus.CREATED,
        }
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_comment_form_valid(self):
        form_data = {
            'message': 'Test comment',
            'user': self.user.id,
            'task': self.task.id,
        }
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())