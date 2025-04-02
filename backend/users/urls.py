from django.urls import path
from . import views

print('work2')
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
]
