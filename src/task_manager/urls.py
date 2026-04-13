from django.urls import path
from task_manager.views import home, tasks, user_tasks
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path('', home , name = 'home'),
    path('tasks/', tasks , name = 'tasks'),
    path('users/<int:user_id>', user_tasks , name = 'user_tasks'),
] + debug_toolbar_urls()
