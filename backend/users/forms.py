from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm
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
                'placeholder': 'Введите пароль' 
                if field_name == 'password1' else 'Повторите пароль'
            })

        
class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'input', 'placeholder': 'Имя пользователя'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'input', 'placeholder': 'Пароль'})
    )


class UserProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = [
            'username', 'avatar', 'first_name', 'last_name',
            'middle_name', 'email', 'phone_number', 'telegram_username']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(self.fields['first_name'].widget.attrs)
        for field_name in self.fields:            
            self.fields[field_name].widget.attrs.update({
                'class': 'input',
            })


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'input',
                'placeholder': self.fields[field].label
            })
