from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('tasks/<int:task_id>/', views.task_list, name='task_list_child'),
    path('create/', views.create_task, name='create_task'),
    path('create/<int:task_id>/', views.task_list, name='create_task_child'),
    # сюда позже добавим task_list и другие представления

    path('tasks/<int:task_id>/status/<int:status_id>/', views.complete_task, name='complete_task'),
    path('<int:task_id>/edit/', views.edit_task, name='edit_task'),
    path('<int:task_id>/edit_parent/', views.edit_parent_task, name='edit_parent_task'),
    path('tasks/<int:task_id>/del/', views.del_task, name='del_task'),
    
    # шаринг задачь
    path('tasks/<int:task_id>/share/<int:user_id>/', views.share_task, name='share_task'),
    path('tasks/<int:task_id>/unshare/<int:user_id>/', views.unshare_task, name='unshare_task'),

    # сохранение сортировки
    path('tasks/reorder/', views.reorder_tasks, name='reorder_tasks'),

    # Урлы для помощи
    path('form-help/parent/<int:task_id>', views.parent_form_view, name='help-parentform'),
    # path('error/', views.error, name='error'),
]
