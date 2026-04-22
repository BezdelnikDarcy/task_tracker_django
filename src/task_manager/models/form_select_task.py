from django import forms
from task_manager.models import Tasks


class SelectTaskForm(forms.Form):
    task = forms.ModelChoiceField(label="Выберите задачу",
                                  queryset=Tasks.objects.all(),
                                  )