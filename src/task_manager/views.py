from urllib import request

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.cache import cache
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.list import ListView
from task_manager.models import Tasks, Comments
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from task_manager.models.forms import TaskForm, CommentForm, SelectTaskForm, AttachmentsForm
from account.models.users import User
from django.views.decorators.cache import cache_page
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_not_required


# MTV

class HomePageView(TemplateView):
    template_name = "home.html"

# def home(request):
#     return render(request, 'home.html')


# def comments(request):
#     context = {
#         'comments' : Comments.objects.select_related('user','task').all(),
#     }
#     return render(request, 'comments.html', context=context)
# @cache_page(60*30)

class CommentsListView(LoginRequiredMixin, ListView):
    template_name = "comments.html"
    model = Comments
    paginate_by = 15
    context_object_name = 'comments'
    def get_queryset(self):
        return Comments.objects.select_related('user','task').all()

# def tasks(request):
#     context = {
#         "tasks": Tasks.objects.prefetch_related("comments","attachments").all()
#     }
#     return render(request,"tasks.html",context=context)
# @cache_page(60*30)
@method_decorator(login_not_required, name='dispatch')
class TasksView(ListView):
    template_name = "tasks.html"
    model = Tasks
    paginate_by = 10
    context_object_name = "tasks"
    def get_queryset(self):
        return Tasks.objects.task_optimization()


class UserTasksDetailView(LoginRequiredMixin, DetailView):
    template_name = "user_tasks.html"
    model = User
    pk_url_kwarg = 'user_id'

    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.object.id
        context["tasks"] = Tasks.objects.filter(assignee__id=user_id).all()
        context["id"] = user_id
        return context


# def user_tasks(request, user_id):
#
#     context = {
#         "tasks": Tasks.objects.filter(assignee__id=user_id).all(),
#         "id" : user_id,
#     }
#     return render(request, 'user_tasks.html', context=context)


class CreateTaskFormView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'task_manager.add_tasks'
    template_name = "create_task.html"
    form_class = TaskForm
    success_url = reverse_lazy("tasks")

    def form_valid(self, form):
        response = super().form_valid(form)
        cache.clear()
        return response


# def create_task(request):
#     if request.method == "POST":
#         form = TaskForm(request.POST)
#         if form.is_valid():
#             form.save()
#             cache.clear()
#             return HttpResponseRedirect(reverse('tasks'))
#     else:
#         form = TaskForm()
#
#     return render(request, 'create_task.html', {'form': form})

class CreateCommentFormView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'task_manager.add_comments'
    template_name = "create_comment.html"
    form_class = CommentForm
    success_url = reverse_lazy("comments")

    def form_valid(self, form):
        response = super().form_valid(form)
        cache.clear()
        return response


# def create_comment(request):
#     if request.method == "POST":
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             Comments.objects.create(message = request.POST['message'],
#                                     user=User.objects.get(id=int(request.POST['user'])),
#                                     task=Tasks.objects.get(id=int(request.POST['task'])),
#                                     )
#             cache.clear()
#             return HttpResponseRedirect(reverse('comments'))
#     else:
#         form = CommentForm()
#
#     return render(request, 'create_comment.html', {'form': form})

@login_required
@permission_required('task_manager.change_tasks')
def select_task(request):
    if request.method == "POST":
        task_id = request.POST.get('task')
        return HttpResponseRedirect(reverse('edit_task', kwargs={'task_id' : task_id}))
    else:
        form = SelectTaskForm()

    return render(request, 'select_task.html', {'form': form})
@login_required
@permission_required('task_manager.change_tasks')
def edit_task(request, **kwargs):
    task = Tasks.objects.get(id=kwargs['task_id'])
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            cache.clear()
            return HttpResponseRedirect(reverse('tasks'))
    else:
        form = TaskForm(instance=task)
    return render(request, 'edit_task.html', {'form': form})

class CreateAttachmentsFormView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'task_manager.add_attachments'
    template_name = "create_attachment.html"
    form_class = AttachmentsForm
    success_url = reverse_lazy("tasks")

    def form_valid(self, form):
        response = super().form_valid(form)
        cache.clear()
        return response


# def create_attachment(request):
#     if request.method == "POST":
#         form = AttachmentsForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             cache.clear()
#             return HttpResponseRedirect(reverse('tasks'))
#     else:
#         form = AttachmentsForm()
#
#     return render(request, 'create_attachment.html', {'form': form})

