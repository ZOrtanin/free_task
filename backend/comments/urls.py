from django.urls import path
from . import views

urlpatterns = [
    path('delete/<int:comment_id>/', views.task_del, name='delete_comment'),
]