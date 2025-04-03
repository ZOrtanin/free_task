from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import CustomLoginView

print('work2')
urlpatterns = [
    #path('login/', auth_views.LoginView.as_view(template_name='users/login.html')),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', views.register, name='register'),
]
