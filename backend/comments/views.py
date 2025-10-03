from django.shortcuts import render, get_object_or_404, redirect
from tasks.models import Task
from comments.forms import CommentForm
from .models import Comment


def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    comments = task.comments.all().order_by('-created_at')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.task = task
            comment.save()
            return redirect('task_detail', pk=task.pk)
    else:
        form = CommentForm()

    return render(request, 'tasks/task.html', {'task': task, 'comments': comments, 'form': form})


def comment_del(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    task_id = comment.task.id
    
    if comment.user == request.user or request.user.is_superuser:
        comment.delete()

    return redirect('task_list_child', task_id=task_id)
    # return render(request, 'tasks/task.html')


def add_comments_task(request, task_id, parent_task):

    if task_id:
        comments = parent_task.comments.all().order_by('-created_at')
        task_comment = parent_task

        if request.method == 'POST':
            form_comment = CommentForm(request.POST)

            if form_comment.is_valid():
                print(form_comment)
                comment = form_comment.save(commit=False)
                comment.user = request.user
                comment.task = task_comment
                comment.save()
                # return redirect('task_detail', pk=task.pk)
        else:
            form_comment = CommentForm()

        data_comments = {
            'comments': comments,
            'form': form_comment,
            }

        return data_comments
