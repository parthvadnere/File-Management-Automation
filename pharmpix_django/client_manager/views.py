# client_manager/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect, FileResponse
from django.urls import reverse
from django.contrib import messages
from client_manager.models import Client, Path, Task, OutputConfig, DownloadedFile
from client_manager.forms import ClientForm, PathForm, TaskForm, OutputConfigForm
from client_manager.tasks import download_files_task
from celery.result import AsyncResult
import logging
import os

logger = logging.getLogger(__name__)

# Dashboard View
def dashboard(request):
    clients_count = Client.objects.count()
    tasks_count = Task.objects.count()
    paths_count = Path.objects.count()
    configs_count = OutputConfig.objects.count()
    return render(request, 'client_manager/dashboard.html', {
        'clients_count': clients_count,
        'tasks_count': tasks_count,
        'paths_count': paths_count,
        'configs_count': configs_count,
    })

# Existing Views (Updated for Messages and Context)
def client_list(request):
    clients = Client.objects.all()
    return render(request, 'client_manager/client_list.html', {'clients': clients})

def download_files(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    logger.info(f"download_files - client_id: {client_id}, client: {client.name}")
    
    task = download_files_task.delay(client_id)
    logger.info(f"Task started with ID: {task.id}")
    
    request.session['task_id'] = task.id
    return redirect('download_status', client_id=client_id)

def download_status(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    task_id = request.session.get('task_id')
    if not task_id:
        logger.error("No task_id found in session")
        return render(request, 'client_manager/download_status.html', {
            'client': client,
            'task_id': None,
            'error': "No task ID found. Please try again."
        })
    
    logger.info(f"Checking status for task_id: {task_id}")
    return render(request, 'client_manager/download_status.html', {
        'client': client,
        'task_id': task_id,
    })

def get_task_status(request):
    task_id = request.GET.get('task_id')
    if not task_id:
        return JsonResponse({'status': 'Failed', 'message': 'No task ID provided'})
    
    task = AsyncResult(task_id)
    logger.info(f"Task {task_id} state: {task.state}")
    
    if task.state == 'PENDING':
        response = {'status': 'In Progress', 'message': 'Download in progress...'}
    elif task.state == 'STARTED':
        response = {'status': 'In Progress', 'message': 'Download started...'}
    elif task.state == 'SUCCESS':
        result = task.result
        response = {'status': result['status'], 'message': result['message']}
    elif task.state == 'FAILURE':
        result = task.result
        response = {'status': 'Failed', 'message': f'Task failed: {str(result)}'}
    else:
        response = {'status': 'Failed', 'message': f'Unknown task state: {task.state}'}
    
    logger.info(f"Task status response: {response}")
    return JsonResponse(response)

# Client CRUD Views
def manage_clients(request):
    clients = Client.objects.all()
    return render(request, 'client_manager/manage_clients.html', {'clients': clients})

def add_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Client added successfully.")
            return redirect('manage_clients')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ClientForm()
    return render(request, 'client_manager/client_form.html', {'form': form, 'action': 'Add'})

def edit_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, "Client updated successfully.")
            return redirect('manage_clients')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ClientForm(instance=client)
    return render(request, 'client_manager/client_form.html', {'form': form, 'action': 'Edit'})

def delete_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    if request.method == 'POST':
        client.delete()
        messages.success(request, "Client deleted successfully.")
        return redirect('manage_clients')
    return render(request, 'client_manager/confirm_delete.html', {'object': client, 'type': 'Client'})

def client_details(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    paths = Path.objects.filter(client=client)
    output_configs = OutputConfig.objects.filter(client=client)
    downloaded_files = DownloadedFile.objects.filter(client=client)
    return render(request, 'client_manager/client_details.html', {
        'client': client,
        'paths': paths,
        'output_configs': output_configs,
        'downloaded_files': downloaded_files,
    })

# Path CRUD Views (Updated for Nested Structure)
def manage_paths(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    paths = Path.objects.filter(client=client)
    return render(request, 'client_manager/manage_paths.html', {'client': client, 'paths': paths})

def add_path(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    if request.method == 'POST':
        form = PathForm(request.POST)
        if form.is_valid():
            path = form.save(commit=False)
            path.client = client
            path.save()
            messages.success(request, "Path added successfully.")
            return redirect('manage_paths', client_id=client_id)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PathForm(initial={'client': client})
    return render(request, 'client_manager/path_form.html', {'form': form, 'action': 'Add', 'client': client})

def edit_path(request, client_id, path_id):
    client = get_object_or_404(Client, id=client_id)
    path = get_object_or_404(Path, id=path_id, client=client)
    if request.method == 'POST':
        form = PathForm(request.POST, instance=path)
        if form.is_valid():
            form.save()
            messages.success(request, "Path updated successfully.")
            return redirect('manage_paths', client_id=client_id)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PathForm(instance=path)
    return render(request, 'client_manager/path_form.html', {'form': form, 'action': 'Edit', 'client': client})

def delete_path(request, client_id, path_id):
    client = get_object_or_404(Client, id=client_id)
    path = get_object_or_404(Path, id=path_id, client=client)
    if request.method == 'POST':
        path.delete()
        messages.success(request, "Path deleted successfully.")
        return redirect('manage_paths', client_id=client_id)
    return render(request, 'client_manager/confirm_delete.html', {'object': path, 'type': 'Path', 'client': client})

# Task CRUD Views
def manage_tasks(request):
    tasks = Task.objects.all()
    return render(request, 'client_manager/manage_tasks.html', {'tasks': tasks})

def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Task added successfully.")
            return redirect('manage_tasks')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = TaskForm()
    return render(request, 'client_manager/task_form.html', {'form': form, 'action': 'Add'})

def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Task updated successfully.")
            return redirect('manage_tasks')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = TaskForm(instance=task)
    return render(request, 'client_manager/task_form.html', {'form': form, 'action': 'Edit'})

def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        task.delete()
        messages.success(request, "Task deleted successfully.")
        return redirect('manage_tasks')
    return render(request, 'client_manager/confirm_delete.html', {'object': task, 'type': 'Task'})

# OutputConfig CRUD Views (Updated for Nested Structure)
def manage_output_configs(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    configs = OutputConfig.objects.filter(client=client)
    return render(request, 'client_manager/manage_output_configs.html', {'client': client, 'configs': configs})

def add_output_config(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    if request.method == 'POST':
        form = OutputConfigForm(request.POST)
        if form.is_valid():
            config = form.save(commit=False)
            config.client = client
            config.save()
            messages.success(request, "Output Config added successfully.")
            return redirect('manage_output_configs', client_id=client_id)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = OutputConfigForm(initial={'client': client})
    return render(request, 'client_manager/output_config_form.html', {'form': form, 'action': 'Add', 'client': client})

def edit_output_config(request, client_id, config_id):
    client = get_object_or_404(Client, id=client_id)
    config = get_object_or_404(OutputConfig, id=config_id, client=client)
    if request.method == 'POST':
        form = OutputConfigForm(request.POST, instance=config)
        if form.is_valid():
            form.save()
            messages.success(request, "Output Config updated successfully.")
            return redirect('manage_output_configs', client_id=client_id)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = OutputConfigForm(instance=config)
    return render(request, 'client_manager/output_config_form.html', {'form': form, 'action': 'Edit', 'client': client})

def delete_output_config(request, client_id, config_id):
    client = get_object_or_404(Client, id=client_id)
    config = get_object_or_404(OutputConfig, id=config_id, client=client)
    if request.method == 'POST':
        config.delete()
        messages.success(request, "Output Config deleted successfully.")
        return redirect('manage_output_configs', client_id=client_id)
    return render(request, 'client_manager/confirm_delete.html', {'object': config, 'type': 'Output Config', 'client': client})

def view_file(request, file_id):
    downloaded_file = get_object_or_404(DownloadedFile, id=file_id)
    return FileResponse(downloaded_file.file, as_attachment=False, filename=downloaded_file.original_filename)

def replace_file(request, file_id):
    downloaded_file = get_object_or_404(DownloadedFile, id=file_id)
    if request.method == 'POST':
        if 'file' in request.FILES:
            new_file = request.FILES['file']
            downloaded_file.file.delete()  # Delete the old file
            downloaded_file.file.save(new_file.name, new_file, save=True)
            downloaded_file.original_filename = new_file.name
            downloaded_file.file_type = os.path.splitext(new_file.name)[1].lstrip('.')
            downloaded_file.save()
            messages.success(request, "File replaced successfully.")
        else:
            messages.error(request, "No file uploaded.")
        return redirect('client_details', client_id=downloaded_file.client.id)
    return render(request, 'client_manager/replace_file.html', {'downloaded_file': downloaded_file})

def delete_file(request, file_id):
    downloaded_file = get_object_or_404(DownloadedFile, id=file_id)
    client_id = downloaded_file.client.id
    if request.method == 'POST':
        downloaded_file.file.delete()  # Delete the file from storage
        downloaded_file.delete()  # Delete the database record
        messages.success(request, "File deleted successfully.")
        return redirect('client_details', client_id=client_id)
    return render(request, 'client_manager/confirm_delete.html', {
        'object': downloaded_file,
        'type': 'Downloaded File',
        'client': downloaded_file.client
    })