from django import forms
from task_manager.models import Tasks
from django.core.exceptions import ValidationError
from django.forms import Textarea


class TaskForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ["name","description", "priority", "status"]
        widgets = {
            'description': Textarea(attrs={'rows': 5, 'cols': 50}),
        }


    def clean(self):
        description = self.cleaned_data.get('description')
        priority = self.cleaned_data.get('priority')

        if not description and priority > 3:
            raise ValidationError("Задача без описания не может иметь высокий приоритет")
