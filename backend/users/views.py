from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm, CustomLoginForm, UserProfileForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required


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


@login_required
def dashboard_view(request):
    return render(request, 'users/dashboard.html')


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # После сохранения редиректим обратно на профиль
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'users/profile.html', {'form': form})