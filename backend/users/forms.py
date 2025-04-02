from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    # middle_name = forms.CharField(
    #     max_length=100, 
    #     required=False, 
    #     label='Отчество')
    # password1 = forms.CharField(
    #     label="Пароль",
    #     widget=forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'Введите пароль'})
    # )

    class Meta:
        model = User

        fields = (
            'username',
            )

        widgets = {
            'username': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Введите логин'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ['password1', 'password2']:
            self.fields[field_name].widget.attrs.update({
                'class': 'input',
                'placeholder': 'Введите пароль' if field_name == 'password1' else 'Повторите пароль'
            })
        
