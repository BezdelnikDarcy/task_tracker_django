from django.urls import path, include
from task_manager.views import HomePageView, TasksView, UserTasksDetailView, CommentsListView, CreateCommentFormView, CreateTaskFormView, edit_task, select_task, CreateAttachmentsFormView
from debug_toolbar.toolbar import debug_toolbar_urls


urlpatterns = [
    path('', HomePageView.as_view() , name = 'home'),
    path('tasks/', TasksView.as_view() , name = 'tasks'),
    path('comments/', CommentsListView.as_view(), name = 'comments'),
    path('users/<int:user_id>', UserTasksDetailView.as_view() , name = 'user_tasks'),
    path('create_comment', CreateCommentFormView.as_view(), name = 'create_comment'),
    path('create_task', CreateTaskFormView.as_view(), name='create_task'),
    path('select_task', select_task, name='select_task'),
    path('edit_task/<int:task_id>', edit_task, name='edit_task'),
    path('create_attachment', CreateAttachmentsFormView.as_view(), name='create_attachment'),
    path('api/', include('task_manager.v1.urls')),
] + debug_toolbar_urls()
