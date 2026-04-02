from django.urls import path
from task_manager.views import home, tasks, users
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path('', home , name = 'home'),
    path('tasks/', tasks , name = 'tasks'),
    path('users/', users , name = 'users'),
] + debug_toolbar_urls()
