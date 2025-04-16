from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'deadline']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control input'}),
            'description': forms.Textarea(attrs={'class': 'form-control textarea'}),
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local','class': 'input'}),
        }


class ParentTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['deadline', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control input'}),
            'description': forms.Textarea(attrs={'class': 'form-control textarea'}),
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local','class': 'input'}),
        }
