from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator


class TaskForm(forms.ModelForm):
    name = forms.CharField(label="task name", max_length=100)
    priority = forms.IntegerField(
        label="task priority",
        validators=[MinValueValidator(0),
                    MaxValueValidator(5)],
    )