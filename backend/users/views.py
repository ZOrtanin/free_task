from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm, CustomLoginForm, UserProfileForm, CustomPasswordChangeForm
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy


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
def task_view(request):
    return render(request, 'users/task.html')


@login_required
def dashboard_view(request):
    return render(request, 'users/dashboard.html')


@login_required
def schedule_view(request):
    return render(request, 'users/schedule.html')


@login_required
def statistics_view(request):
    return render(request, 'users/statistics.html')


@login_required
def profile(request):
    return render(request, 'users/profile.html')


@login_required
def settings(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('settings')  # После сохранения редиректим обратно на настройки
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'users/settings.html', {'form': form})


class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'users/password_change.html'
    success_url = reverse_lazy('profile')  
    # Или другой URL, куда перенаправить после успешной смены пароля
