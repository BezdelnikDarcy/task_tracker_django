from django.urls import path
from task_manager.views import home, tasks, user_tasks, comments, create_comment, create_task, edit_task, select_task, create_attachment
from debug_toolbar.toolbar import debug_toolbar_urls


urlpatterns = [
    path('', home , name = 'home'),
    path('tasks/', tasks , name = 'tasks'),
    path('comments/', comments, name = 'comments'),
    path('users/<int:user_id>', user_tasks , name = 'user_tasks'),
    path('create_comment', create_comment, name = 'create_comment'),
    path('create_task', create_task, name='create_task'),
    path('select_task', select_task, name='select_task'),
    path('edit_task/<int:task_id>', edit_task, name='edit_task'),
    path('create_attachment', create_attachment, name='create_attachment'),
] + debug_toolbar_urls()
