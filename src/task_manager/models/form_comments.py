from django import forms
from task_manager.models import Tasks
from account.models.users import User

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