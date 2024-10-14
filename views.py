from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from todo.forms import TaskForm
from .models import Task, TaskHistory

def task_list(request):
    tasks = Task.objects.all().order_by('progress')  # Fetch all tasks and order by progress
    form = TaskForm()

    # Count tasks by status
    pending_count = tasks.filter(status='pending').count()
    in_progress_count = tasks.filter(status='in_progress').count()
    completed_count = tasks.filter(status='completed').count()

    # Pass tasks and counts to the template
    return render(request, 'list.html', {
        'tasks': tasks,
        'form': form,
        'pending_count': pending_count,
        'in_progress_count': in_progress_count,
        'completed_count': completed_count,
    })

def task_create(request):
    if request.method == 'POST':
        task_name = request.POST.get('task_name')
        task_id = request.POST.get('task_id')
        task_status = request.POST.get('task_status')

        if task_id:
            task = get_object_or_404(Task, pk=task_id)
            task.name = task_name
            task.status = task_status
        else:
            task = Task.objects.create(
                name=task_name,
                status=task_status
            )
        task.save()

        return JsonResponse({
            'pk': task.pk,
            'name': task.name,
            'progress': task.progress,
            'status': task.status
        })

def update_task(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == 'POST':
        task_name = request.POST.get('task_name', task.name)
        increment = request.POST.get('increment')

        task.name = task_name

        if increment:
            increment = int(increment)
            task.progress += increment
            task.progress = max(0, min(100, task.progress))

        if task.progress == 100:
            task.status = 'completed'
        elif task.progress > 0:
            task.status = 'in_progress'
        else:
            task.status = 'pending'

        task.save()

        return JsonResponse({
            'pk': task.pk,
            'name': task.name,
            'progress': task.progress,
            'status': task.status
        })

    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def delete_task(request, task_id):
    if request.method == "POST":
        try:
            task = Task.objects.get(id=task_id)
            TaskHistory.objects.create(name=task.name, status=task.status, progress=task.progress)
            task.delete()
            return JsonResponse({'status': 'success'})
        except Task.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Task not found'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

@csrf_exempt
def reset_task(request, task_id):
    if request.method == "POST":
        try:
            task = Task.objects.get(id=task_id)
            task.progress = 0
            task.status = 'pending'
            task.save()

            return JsonResponse({'status': 'success', 'progress': task.progress, 'name': task.name})
        except Task.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Task not found'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

@csrf_exempt
def update_task_progress(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        increment = request.POST.get('increment')

        if not task_id or not increment:
            return JsonResponse({'error': 'Task ID or increment missing'}, status=400)

        try:
            task = Task.objects.get(pk=task_id)
            task.progress += int(increment)
            task.progress = max(0, min(100, task.progress))

            if task.progress == 100:
                task.status = 'completed'
            elif task.progress > 0:
                task.status = 'in_progress'
            else:
                task.status = 'pending'

            task.save()

            return JsonResponse({'status': task.status, 'progress': task.progress, 'name': task.name})
        except Task.DoesNotExist:
            return JsonResponse({'error': 'Task not found'}, status=404)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def task_history(request):
    task_histories = TaskHistory.objects.all().order_by('-id')
    return render(request, 'history.html', {'task_histories': task_histories})
def complete_task(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        task = get_object_or_404(Task, pk=task_id)
        task.progress = 100  # Or set task.status = 'completed' based on your model
        task.save()
        return redirect('task_list')  # Redirect to your task list page

@csrf_protect
def edit_task(request, task_id):
    if request.method == 'POST':
        try:
            # Fetch the task using get_object_or_404 for better error handling
            task = get_object_or_404(Task, pk=task_id)
            
            # Update the task name
            task.name = request.POST.get('name', task.name)
            
            # Save the task
            task.save()

            # Send success response
            return JsonResponse({'status': 'success', 'message': 'Task updated successfully.'})

        except Task.DoesNotExist:
            # Return error if task is not found
            return JsonResponse({'status': 'error', 'message': 'Task not found.'}, status=404)
    
    # If the request is not a POST, return an error
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)
