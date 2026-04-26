from django import forms
from task_manager.models import Tasks, Attachments
from django.core.exceptions import ValidationError
from django.forms import Textarea
from account.models.users import User


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

class SelectTaskForm(forms.Form):
    task = forms.ModelChoiceField(label="Выберите задачу",
                                  queryset=Tasks.objects.all(),
                                  )

class CommentForm(forms.Form):
    message = forms.CharField(label="Комментарий",
                              widget=forms.Textarea,
                              max_length=256,
                              )
    user = forms.ModelChoiceField(label="Пользователь",
                                  queryset=User.objects.all(),
                                  widget=forms.Select(attrs={'class': 'user-select'}),
                                  )
    task = forms.ModelChoiceField(label="Задача",
                                  queryset=Tasks.objects.all(),
                                  )

class AttachmentsForm(forms.ModelForm):
    class Meta:
        model = Attachments
        fields = ["name", "task","file", "picture",]