from django.urls import path
from task_manager.v1.views.task import TaskListApiView, TaskDetailApiView
from task_manager.v1.views.tag import tag_list, tag_detail
from task_manager.v1.views.attachment import AttachmentListApiView, AttachmentDetailApiView
from task_manager.v1.views.comment import CommentListApiView, CommentDetailApiView
from task_manager.v1.views.project import ProjectListApiView, ProjectDetailApiView
from task_manager.v1.views.project_detail import ProjectDetailsListApiView, ProjectDetailsDetailApiView


urlpatterns = [
    path("tasks/", TaskListApiView.as_view()),
    path("tasks/<int:pk>/", TaskDetailApiView.as_view()),
    path("tags/", tag_list),
    path("tags/<int:pk>/", tag_detail),
    path("attachments/", AttachmentListApiView.as_view()),
    path("attachments/<int:pk>/", AttachmentDetailApiView.as_view()),
    path("comments/", CommentListApiView.as_view()),
    path("comments/<int:pk>/", CommentDetailApiView.as_view()),
    path("projects/", ProjectListApiView.as_view()),
    path("projects/<int:pk>/", ProjectDetailApiView.as_view()),
    path("project_details/", ProjectDetailsListApiView.as_view()),
    path("project_details/<int:pk>/", ProjectDetailsDetailApiView.as_view()),

]