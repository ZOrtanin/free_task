from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
#from .views import CustomLoginView

print('work2')
urlpatterns = [
    #path('login/', auth_views.LoginView.as_view(template_name='users/login.html')),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile/', views.profile, name='profile'),

]
