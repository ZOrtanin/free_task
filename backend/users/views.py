from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, get_user_model
from .forms import CustomUserCreationForm, CustomLoginForm, UserProfileForm, CustomPasswordChangeForm

# from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.decorators import login_required

from django.urls import reverse_lazy
from .utils import generate_avatar_image
from .models import Follow
from tasks.models import Task
from django.db.models import Q

from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.utils import timezone
from datetime import timedelta

# Create your views here.
class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = 'users/login.html'


# def login_view(request):
#     return render(request, 'users/login.html')


def register(request):

    avatar_path = generate_avatar_image()
    print(avatar_path)
    # form = CustomUserCreationForm(initial={'avatar': avatar_path})

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            
            user = form.save()

            user.avatar.name = avatar_path  # Указываем путь относительно MEDIA_ROOT
            user.save()

            login(request, user)  # Автоматический вход после регистрации
            return redirect('dashboard')  # Перенаправляем на домашнюю страницу (или другую)
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/register.html', {'form': form, 'avatar_path': avatar_path})


@login_required
def task_view(request):
    return render(request, 'users/task.html')


@login_required
def dashboard_view(request):

    tasks = Task.objects.filter(
        Q(author=request.user) | Q(shared_with=request.user),
        parent__isnull=False
        )

    month_ago = timezone.now() - timedelta(days=4)
    now = timezone.now() - timedelta(days=1)

    user = get_object_or_404(User, username=request.user)

    followers = Follow.objects.filter(following=user).select_related('follower').count()
    following = Follow.objects.filter(follower=user).select_related('following').count()

    context = {
        'last_tasks': tasks.order_by('-created_at')[:7],
        'run_tasks': tasks.filter(updated_at__lt=now)[:7],
        'old_tasks': tasks.filter(updated_at__lt=month_ago)[:7],
        'end_task': tasks.filter(status_id=2).order_by('updated_at').reverse()[:7],
        'end_task_count': tasks.filter(status_id=2).count(),
        'count_task': tasks.count(),       
        'followers': followers,
        'following': following,

    }

    return render(request, 'users/dashboard.html', context)


@login_required
def schedule_view(request):
    return render(request, 'users/schedule.html')


@login_required
def statistics_view(request):
    return render(request, 'users/statistics.html')


def user_page(request, user_name):

    user = get_object_or_404(User, username=user_name)

    tasks = Task.objects.filter(
        author=user       
        ).order_by('-created_at').reverse()[:7]
    
    # Все, кто следят за user
    followers_qs = Follow.objects.filter(following=user).select_related('follower')
    followers = [f.follower for f in followers_qs]

    # Все, за кем следит user
    following_qs = Follow.objects.filter(follower=user).select_related('following')
    following = [f.following for f in following_qs]

    # Только те, кто следят за пользователем
    one_way_followers = [user for user in followers if user not in following]

    following_ads = user.following.values_list('following_id', flat=True)

    context = {
        'user_page': True,
        'profile_user': user,
        'followers': followers,             # Все подписчики
        'following': following,             # Все, за кем он следит        
        'one_way_followers': one_way_followers,  # Односторонние подписки
        'following_ads': list(following_ads),
        'tasks': tasks,
    }

    return render(request, 'users/profile/profile.html', context)


@login_required
def profile(request):

    tasks = Task.objects.filter(
        author=request.user        
        ).order_by('-created_at').reverse()[:7]

    user = get_object_or_404(User, username=request.user.username)
    # followers = Follow.objects.filter(following=user).select_related("follower")
    # follower_users = [f.follower for f in followers]

    # Все, кто следят за user
    followers_qs = Follow.objects.filter(following=user).select_related('follower')
    followers = [f.follower for f in followers_qs]

    # Все, за кем следит user
    following_qs = Follow.objects.filter(follower=user).select_related('following')
    following = [f.following for f in following_qs]

    # Только те, кто следят за пользователем
    one_way_followers = [user for user in followers if user not in following]

    following_ads = user.following.values_list('following_id', flat=True)

    context = {
        'profile_user': user,
        'followers': followers,             # Все подписчики
        'following': following,             # Все, за кем он следит        
        'one_way_followers': one_way_followers,  # Односторонние подписки
        'following_ads': list(following_ads),
        'tasks': tasks,
    }

    return render(request, 'users/profile/profile.html', context)


@login_required
def settings(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('settings')  # После сохранения редиректим обратно на настройки
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'users/profile/settings.html', {'form': form})


class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'users/profile/password_change.html'
    success_url = reverse_lazy('profile')  
    # Или другой URL, куда перенаправить после успешной смены пароля


# ======= Подписки =======
User = get_user_model()
# подписка пользователя
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    if request.user != user_to_follow:  # предотвращаем подписку на самого себя
        Follow.objects.get_or_create(follower=request.user, following=user_to_follow)
    return redirect('profile')


# отписка пользователя
def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(User, id=user_id)
    Follow.objects.filter(follower=request.user, following=user_to_unfollow).delete()
    return redirect('profile')


class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users/profile/popup/user_list.html'
    context_object_name = 'users'

    def get_queryset(self):        
        return User.objects.exclude(id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        following_ids = Follow.objects.filter(follower=self.request.user).values_list('following_id', flat=True)
        context['following_ids'] = set(following_ids)
        return context
