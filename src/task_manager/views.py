from django.http import HttpResponse
from task_manager.models import Tasks
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

# MTV
def home(request):
    return render(request, 'home.html')


def tasks(request):
    context = {
        "tasks": Tasks.objects.prefetch_related("comments").all()
    }
    return render(request,"tasks.html",context=context)


def user_tasks(request, user_id, ):

    context = {
        "tasks": Tasks.objects.filter(assignee__id=user_id).all(),
        "id" : user_id,
    }
    return render(request, 'user_tasks.html', context=context)
