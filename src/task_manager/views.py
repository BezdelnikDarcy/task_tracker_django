from django.http import HttpResponse
from task_manager.models import Tasks, Comments
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from task_manager.models.forms import TaskForm, CommentForm, SelectTaskForm, AttachmentsForm
from account.models.users import User



# MTV
def home(request):
    return render(request, 'home.html')

def comments(request):
    context = {
        'comments' : Comments.objects.select_related('user','task').all(),
    }
    return render(request, 'comments.html', context=context)

def tasks(request):
    context = {
        "tasks": Tasks.objects.prefetch_related("comments","attachments").all()
    }
    return render(request,"tasks.html",context=context)


def user_tasks(request, user_id):

    context = {
        "tasks": Tasks.objects.filter(assignee__id=user_id).all(),
        "id" : user_id,
    }
    return render(request, 'user_tasks.html', context=context)

def create_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('tasks'))
    else:
        form = TaskForm()

    return render(request, 'create_task.html', {'form': form})

def create_comment(request):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            Comments.objects.create(message = request.POST['message'],
                                    user=User.objects.get(id=int(request.POST['user'])),
                                    task=Tasks.objects.get(id=int(request.POST['task'])),
                                    )
            return HttpResponseRedirect(reverse('comments'))
    else:
        form = CommentForm()

    return render(request, 'create_comment.html', {'form': form})

def select_task(request):
    if request.method == "POST":
        task_id = request.POST.get('task')
        return HttpResponseRedirect(reverse('edit_task', kwargs={'task_id' : task_id}))
    else:
        form = SelectTaskForm()

    return render(request, 'select_task.html', {'form': form})

def edit_task(request, **kwargs):
    task = Tasks.objects.get(id=kwargs['task_id'])
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('tasks'))
    else:
        form = TaskForm(instance=task)
    return render(request, 'edit_task.html', {'form': form})

def create_attachment(request):
    if request.method == "POST":
        form = AttachmentsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('tasks'))
    else:
        form = AttachmentsForm()

    return render(request, 'create_attachment.html', {'form': form})
