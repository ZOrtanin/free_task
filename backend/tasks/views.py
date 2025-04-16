from django.shortcuts import render, redirect, get_object_or_404
from .forms import TaskForm, ParentTaskForm
from django.contrib.auth.decorators import login_required
from .models import Task, TaskStatus
from django.db.models import Case, When, IntegerField
from django.db.models import Q


@login_required
def task_list(request, task_id=None):

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
        ).order_by('completed_order', '-created_at')
        breadcrumbs = parent_task.get_breadcrumbs()

        parent_form = ParentTaskForm()

        context = {
            'parent_task': parent_task,
            'breadcrumbs': breadcrumbs,
            'tasks': children,
            'form': form,
            'parent_form': parent_form
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
            ).order_by('completed_order', '-created_at')

        print('tasks ')
        print(tasks)
        for item in tasks:
            print(item.children )

        context = {
            'tasks': tasks,
            'form': form
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
def complete_task(request, task_id, status_id):
    task = get_object_or_404(Task, id=task_id)
    completed_status = get_object_or_404(TaskStatus, id=status_id)  # id статуса "Завершено"

    task.status = completed_status
    task.save()

    return redirect('task_list')  # или куда тебе нужно


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, author=request.user)
    form = TaskForm(request.POST, instance=task)
    if form.is_valid():
        form.save()
    return redirect('task_list')

@login_required
def edit_parent_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, author=request.user)
    form = ParentTaskForm(request.POST, instance=task)
    if form.is_valid():
        form.save()
    return redirect('task_list_child', task_id=task_id)

@login_required
def del_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, author=request.user)
    task.delete()
    return redirect('task_list')
