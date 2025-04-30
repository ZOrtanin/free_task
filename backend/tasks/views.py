from django.shortcuts import render, redirect, get_object_or_404
from .forms import TaskForm, ParentTaskForm
from django.contrib.auth.decorators import login_required
from .models import Task, TaskStatus
from django.db.models import Case, When, IntegerField
from django.db.models import Q

from django.contrib import messages

from django.views.decorators.http import require_POST
from django.http import JsonResponse
import json

from django.contrib.auth import get_user_model
User = get_user_model()

from django.utils import timezone


@login_required
def parent_form_view(request, task_id=None):
    task = get_object_or_404(Task, id=task_id, author=request.user)
    form = ParentTaskForm(request.POST, instance=task)

    context = {
        'form': form,
        }

    return render(request, 'form/parent_form.html', context)


@login_required
def task_list(request, task_id=None, error=None):
    users = User.objects.exclude(id=request.user.id)

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.author = request.user
            task.status_id = 0
            if task_id:
                task.parent_id = task_id  # Привязываем к родителю, если есть
            task.save()
            #return redirect('task_list')  # Заменим позже на нужный URL
            return redirect('task_list_child', task_id=task_id) if task_id else redirect('task_list')
    else:
        form = TaskForm()  

    if task_id:
        # Детальный просмотр задачи и её подзадач
        parent_task = get_object_or_404(Task, id=task_id)
        breadcrumbs = []

        children = parent_task.children.annotate(
            completed_order=Case(
                When(status__name="Завершено", then=1),
                default=0,
                output_field=IntegerField()
            )
        ).order_by('position')
        # ).order_by('completed_order', '-created_at', 'position')

        breadcrumbs = parent_task.get_breadcrumbs()

        parent_form = ParentTaskForm()

        for task in children:
            task.recently_updated = (timezone.now() - task.updated_at).total_seconds() < 600

            if task.children.count() > 0:
                task.icon_child = True

        context = {
            'users': users,
            'parent_task': parent_task,
            'breadcrumbs': breadcrumbs,
            'tasks': children,
            'form': form,
            'parent_form': parent_form,
            'errors': error,            
        }

    else:
        # Общий список задач без родителя                 
        tasks = Task.objects.filter(
                Q(author=request.user) | Q(shared_with=request.user),
                parent__isnull=True
                ).annotate(
                completed_order=Case(
                    When(status__name="Завершено", then=1),
                    default=0,
                    output_field=IntegerField()
                )
            #).order_by('completed_order', '-created_at', 'position').distinct()
            ).order_by('position').distinct()

        for task in tasks:
            task.recently_updated = (timezone.now() - task.updated_at).total_seconds() < 600

            if task.children.count() > 0:
                task.icon_child = True

        context = {
            'tasks': tasks,
            'form': form,
            'errors': error,
        }
    
    return render(request, 'tasks/task.html', context)


@login_required
def create_task(request, task_id=None):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.author = request.user
            task.status_id = 0
            task.save()
            return redirect('task_list')  # Заменим позже на нужный URL
    else:
        form = TaskForm()
    return render(request, 'tasks/create_task.html', {'form': form})


@login_required
def complete_task(request, task_id, status_id, parent_task=None):
    task = get_object_or_404(Task, id=task_id)
    completed_status = get_object_or_404(TaskStatus, id=status_id)  # id статуса "Завершено"

    task.status = completed_status
    position_down = 23

    if task.parent_id is not None:
        position_down = Task.objects.get(id=task.parent_id).children.count()
    else:
        position_down = Task.objects.filter(
                        Q(author=request.user) | Q(shared_with=request.user),
                        parent__isnull=True
                    ).distinct().count()

    if status_id == 2:
        task.position = position_down
    else:
        task.position = 0

    task.save()

    if task.parent_id is None:
        return redirect('task_list')  # или куда тебе нужно
    else:
        return redirect('task_list_child', task_id=task.parent_id)


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, author=request.user)
    form = TaskForm(request.POST, instance=task)
    
    if form.is_valid():
        form.save()

    if task.parent_id is None:
        return redirect('task_list')  # или куда тебе нужно
    else:        
        return redirect('task_list_child', task_id=task.parent_id)


@login_required
def edit_parent_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, author=request.user)
    form = ParentTaskForm(request.POST, instance=task)
    
    if form.is_valid():
        form.save()
        return redirect('task_list_child', task_id=task_id)  

    # for error in form.errors:
    messages.error(request, f"{form.errors}")  

    return redirect('task_list_child', task_id=task_id)


@login_required
def del_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, author=request.user)    

    if task.parent_id is None:
        task.delete()
        return redirect('task_list')  # или куда тебе нужно
    else:
        task.delete()
        return redirect('task_list_child', task_id=task.parent_id)


@login_required
def share_task(request, task_id, user_id):
    task = get_object_or_404(Task, id=task_id, author=request.user)
    user = get_object_or_404(User, id=user_id)
    
    task.shared_with.add(user)
    return redirect('task_list_child', task_id=task.id)


@login_required
def unshare_task(request, task_id, user_id):
    task = get_object_or_404(Task, id=task_id, author=request.user)
    user = get_object_or_404(User, id=user_id)

    # Только автор может управлять доступами
    if task.author != request.user:
        return redirect('task_list')

    task.shared_with.remove(user)
    return redirect('task_list_child', task_id=task.id)


# Сохранение сортировки
@login_required
@require_POST
def reorder_tasks(request):
    data = json.loads(request.body)
    task_ids = data.get('task_ids', [])  # ['3', '2', '5', '1']    

    for index, task_id in enumerate(task_ids):
        Task.objects.filter(id=task_id, author=request.user).update(position=index)

    return JsonResponse({'status': 'ok'})




