from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm, CustomLoginForm
from django.contrib.auth.views import LoginView


# Create your views here.
class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = 'users/login.html'


def login_view(request):
    return render(request, 'users/login.html')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматический вход после регистрации
            return redirect('home')  # Перенаправляем на домашнюю страницу (или другую)
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/register.html', {'form': form})
