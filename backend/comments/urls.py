from django.urls import path
from . import views

urlpatterns = [
    path('delete/<int:comment_id>/', views.comment_del, name='delete_comment'),
]