from django.shortcuts import render
from django.http import HttpResponse

# MTV
def home(request):
    return render(request, 'home.html')

def tasks(request):
    tasks = [
        {"task_name": "Fix login bug", "status": "in progress", "priority": "high"},
        {"task_name": "Create navbar", "status": "done", "priority": "medium"},
        {"task_name": "Write tests", "status": "todo", "priority": "high"},
        {"task_name": "Update documentation", "status": "todo", "priority": "low"},
        {"task_name": "Deploy project", "status": "in progress", "priority": "medium"}
    ]
    context = {
        "tasks": tasks
    }
    return render(request, 'tasks.html', context)

def users(request):
    users = [
        {"id": 0, "name": "Alice", "age": 25},
        {"id": 1,"name": "Bob", "age": 30},
        {"id": 2,"name": "Charlie", "age": 28},
        {"id": 3,"name": "Diana", "age": 22}
    ]
    context = {
        "users": users
    }
    return render(request, 'users.html', context=context)