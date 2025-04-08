from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from .views import CustomPasswordChangeView

print('work2')
urlpatterns = [
    #path('login/', auth_views.LoginView.as_view(template_name='users/login.html')),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register, name='register'),

    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('tasks/', views.task_view, name='tasks'),
    path('schedule/', views.schedule_view, name='schedule'),
    path('statistics/', views.statistics_view, name='statistics'),

    path('profile/', views.profile, name='profile'),
    path('settings/', views.settings, name='settings'),
    path('password/', CustomPasswordChangeView.as_view(), name='password_change'),

]
