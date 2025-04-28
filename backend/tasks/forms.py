from django import forms
from .models import Task
from django.db.models import Case, When, IntegerField
from django.db.models import Q
from django.shortcuts import get_object_or_404


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
        id_task = None
        model = Task
        fields = ['deadline', 'description', 'parent']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control input'}),
            'description': forms.Textarea(attrs={'class': 'form-control textarea'}),
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'input'}),
            
        }
        print('work select 1')

        def __init__(self, *args, **kwargs):
            # Передадим пользователя в форму
            user = kwargs.pop('user', None)  
            current_task = kwargs.pop('current_task', None)
            super().__init__(*args, **kwargs)
            
            print('work select 2')
            
            if user:
                self.fields['parent'].queryset = Task.objects.filter(
                    author=user, 
                    parent__isnull=True
                    )
                if current_task:
                    print('work select 3 ')


