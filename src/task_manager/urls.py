from django.urls import path
from task_manager.views import home, tasks, users

urlpatterns = [
    path('', home , name = 'home'),
    path('tasks/', tasks , name = 'tasks'),
    path('users/', users , name = 'users'),
]
