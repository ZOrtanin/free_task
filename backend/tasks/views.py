from django.shortcuts import render, redirect, get_object_or_404
from .forms import TaskForm
from django.contrib.auth.decorators import login_required
from .models import Task, TaskStatus
from django.db.models import Case, When, IntegerField


@login_required
def create_task(request):
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
def task_list(request):
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
        # tasks = Task.objects.filter(author=request.user).order_by('-created_at')

        tasks = Task.objects.annotate(
                completed_order=Case(
                    When(status__name="Завершено", then=1),
                    default=0,
                    output_field=IntegerField()
                )
            ).order_by('completed_order', '-created_at')
    
    return render(request, 'tasks/task.html', {'tasks': tasks, 'form': form})


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
def del_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, author=request.user)
    task.delete()
    return redirect('task_list')
