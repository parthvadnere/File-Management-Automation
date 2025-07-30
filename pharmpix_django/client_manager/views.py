from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse, FileResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from client_manager.models import Client, Path, Task, OutputConfig, DownloadedFile, FileConfig
from client_manager.forms import ClientForm, PathForm, TaskForm, OutputConfigForm, DownloadForm, FileConfigForm, UploadConfigForm, CustomUserCreationForm
from client_manager.tasks import download_files_task, download_10pm_files_task
from celery.result import AsyncResult
from datetime import datetime
import logging
import os
import mimetypes
import paramiko
from io import BytesIO

logger = logging.getLogger(__name__)

# Authentication Views
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'client_manager/signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # messages.success(request, 'Logged in successfully.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'client_manager/login.html', {'form': form})

def user_logout(request):
    logout(request)
    # messages.success(request, 'Logged out successfully.')
    return redirect('login')

# Dashboard View
@login_required
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

# Existing Views with login_required decorator
@login_required
def client_list(request):
    clients = Client.objects.all()
    return render(request, 'client_manager/client_list.html', {'clients': clients})

@login_required
def download_files(request, client_id, date_filter=None):
    if date_filter:
        try:
            selected_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
        except ValueError:
            selected_date = None
    else:
        selected_date = None

    task = download_files_task.delay(client_id, selected_date=selected_date)
    return redirect(reverse('download_status', args=[client_id]) + f'?task_id={task.id}')

@login_required
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

@login_required
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

@login_required
def manage_clients(request):
    clients = Client.objects.all()
    return render(request, 'client_manager/manage_clients.html', {'clients': clients})

@login_required
def add_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Client created successfully.')
            return redirect('manage_clients')
    else:
        form = ClientForm()
    return render(request, 'client_manager/client_form.html', {'form': form, 'title': 'Add Client'})

@login_required
def edit_client(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, 'Client updated successfully.')
            return redirect('client_details', client_id=client.id)
    else:
        form = ClientForm(instance=client)
    return render(request, 'client_manager/client_form.html', {'form': form, 'title': 'Edit Client'})

@login_required
def delete_client(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    if request.method == 'POST':
        client.delete()
        messages.success(request, 'Client deleted successfully.')
        return redirect('manage_clients')
    return render(request, 'client_manager/client_confirm_delete.html', {'client': client})

@login_required
def client_details(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    paths = Path.objects.filter(client=client)
    output_configs = OutputConfig.objects.filter(client=client)
    file_configs = FileConfig.objects.filter(client=client)

    if request.method == 'POST' and 'download_5pm' in request.POST:
        form_5pm = DownloadForm(request.POST, prefix='5pm')
        if form_5pm.is_valid():
            selected_date = form_5pm.cleaned_data['selected_date']
            selected_date_str = selected_date.strftime('%Y-%m-%d') if selected_date else None
            download_files_task.delay(client_id=client.id, selected_date=selected_date_str)
            messages.success(request, '5PM file download task has been triggered.')
            return redirect('client_details', client_id=client.id)
    else:
        form_5pm = DownloadForm(prefix='5pm')

    # Handle 10PM download
    if request.method == 'POST' and 'download_10pm' in request.POST:
        logger.info(f"10PM download request received for client_id: {client_id}, POST data: {request.POST}")
        form_10pm = DownloadForm(request.POST, prefix='10pm')
        if form_10pm.is_valid():
            logger.info(f"10PM form is valid, selected_date: {form_10pm.cleaned_data['selected_date']}")
            selected_date = form_10pm.cleaned_data['selected_date']
            selected_date_str = selected_date.strftime('%Y-%m-%d') if selected_date else None
            # Pass client_id to the task
            download_10pm_files_task.delay(client_id=client.id, selected_date=selected_date_str)
            messages.success(request, '10PM file download task has been triggered.')
            return redirect('client_details', client_id=client.id)
        else:
            logger.error(f"10PM form validation failed: {form_10pm.errors}")
    else:
        form_10pm = DownloadForm(prefix='10pm')

    downloaded_files = DownloadedFile.objects.filter(client=client).order_by('-downloaded_at')
    
    return render(request, 'client_manager/client_details.html', {
        'client': client,
        'paths': paths,
        'output_configs': output_configs,
        'file_configs': file_configs,
        'downloaded_files': downloaded_files,
        'form_5pm': form_5pm,
        'form_10pm': form_10pm,
    })

@login_required
def add_file_config(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    if request.method == 'POST':
        form = FileConfigForm(request.POST)
        if form.is_valid():
            file_config = form.save(commit=False)
            file_config.client = client
            file_config.save()
            messages.success(request, 'File configuration added successfully.')
            return redirect('client_details', client_id=client.id)
    else:
        form = FileConfigForm()
    return render(request, 'client_manager/file_config_form.html', {'form': form, 'client': client, 'title': 'Add File Configuration'})

@login_required
def edit_file_config(request, config_id):
    file_config = get_object_or_404(FileConfig, pk=config_id)
    if request.method == 'POST':
        form = FileConfigForm(request.POST, instance=file_config)
        if form.is_valid():
            form.save()
            messages.success(request, 'File configuration updated successfully.')
            return redirect('client_details', client_id=file_config.client.id)
    else:
        form = FileConfigForm(instance=file_config)
    return render(request, 'client_manager/file_config_form.html', {'form': form, 'client': file_config.client, 'title': 'Edit File Configuration'})

@login_required
def delete_file_config(request, config_id):
    file_config = get_object_or_404(FileConfig, pk=config_id)
    if request.method == 'POST':
        client_id = file_config.client.id
        file_config.delete()
        messages.success(request, 'File configuration deleted successfully.')
        return redirect('client_details', client_id=client_id)
    return render(request, 'client_manager/file_config_confirm_delete.html', {'file_config': file_config})

@login_required
def manage_paths(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    paths = Path.objects.filter(client=client)
    logger.info(f"manage_paths - client_id: {client_id}, client: {client.name}, paths: {paths}")
    return render(request, 'client_manager/manage_paths.html', {'client': client, 'paths': paths})

@login_required
def add_path(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    if request.method == 'POST':
        form = PathForm(request.POST)
        if form.is_valid():
            path = form.save(commit=False)
            path.client = client
            path.save()
            messages.success(request, 'Path added successfully.')
            return redirect('client_details', client_id=client.id)
    else:
        form = PathForm()
    return render(request, 'client_manager/path_form.html', {'form': form, 'client': client, 'title': 'Add Path'})

@login_required
def edit_path(request, client_id, path_id):
    path = get_object_or_404(Path, pk=path_id, client_id=client_id)
    if request.method == 'POST':
        form = PathForm(request.POST, instance=path)
        if form.is_valid():
            form.save()
            messages.success(request, 'Path updated successfully.')
            return redirect('client_details', client_id=client_id)
    else:
        form = PathForm(instance=path)
    return render(request, 'client_manager/path_form.html', {'form': form, 'client': path.client, 'title': 'Edit Path'})

@login_required
def delete_path(request, client_id, path_id):
    path = get_object_or_404(Path, pk=path_id, client_id=client_id)
    if request.method == 'POST':
        path.delete()
        messages.success(request, 'Path deleted successfully.')
        return redirect('client_details', client_id=client_id)
    return render(request, 'client_manager/path_confirm_delete.html', {'path': path})

@login_required
def manage_tasks(request):
    tasks = Task.objects.all()
    return render(request, 'client_manager/manage_tasks.html', {'tasks': tasks})

@login_required
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

@login_required
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

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        task.delete()
        messages.success(request, "Task deleted successfully.")
        return redirect('manage_tasks')
    return render(request, 'client_manager/confirm_delete.html', {'object': task, 'type': 'Task'})

@login_required
def manage_output_configs(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    configs = OutputConfig.objects.filter(client=client)
    return render(request, 'client_manager/manage_output_configs.html', {'client': client, 'configs': configs})

@login_required
def add_output_config(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    if request.method == 'POST':
        form = OutputConfigForm(request.POST)
        if form.is_valid():
            config = form.save(commit=False)
            config.client = client
            config.save()
            messages.success(request, 'Output configuration added successfully.')
            return redirect('client_details', client_id=client.id)
    else:
        form = OutputConfigForm()
    return render(request, 'client_manager/output_config_form.html', {'form': form, 'client': client, 'title': 'Add Output Config'})

@login_required
def edit_output_config(request, client_id, config_id):
    config = get_object_or_404(OutputConfig, pk=config_id, client_id=client_id)
    if request.method == 'POST':
        form = OutputConfigForm(request.POST, instance=config)
        if form.is_valid():
            form.save()
            messages.success(request, 'Output configuration updated successfully.')
            return redirect('client_details', client_id=client_id)
    else:
        form = OutputConfigForm(instance=config)
    return render(request, 'client_manager/output_config_form.html', {'form': form, 'client': config.client, 'title': 'Edit Output Config'})

@login_required
def delete_output_config(request, client_id, config_id):
    config = get_object_or_404(OutputConfig, pk=config_id, client_id=client_id)
    if request.method == 'POST':
        config.delete()
        messages.success(request, 'Output configuration deleted successfully.')
        return redirect('client_details', client_id=client_id)
    return render(request, 'client_manager/output_config_confirm_delete.html', {'config': config})

@login_required
def client_create(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Client created successfully.')
            return redirect('client_list')
    else:
        form = ClientForm()
    return render(request, 'client_manager/client_form.html', {'form': form, 'title': 'Create Client'})

@login_required
def client_update(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, 'Client updated successfully.')
            return redirect('client_list')
    else:
        form = ClientForm(instance=client)
    return render(request, 'client_manager/client_form.html', {'form': form, 'title': 'Update Client'})

@login_required
def client_delete(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        client.delete()
        messages.success(request, 'Client deleted successfully.')
        return redirect('client_list')
    return render(request, 'client_manager/client_confirm_delete.html', {'client': client})

@login_required
def file_config_list(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    file_configs = FileConfig.objects.filter(client=client)
    return render(request, 'client_manager/file_config_list.html', {'client': client, 'file_configs': file_configs})

@login_required
def file_config_create(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    if request.method == 'POST':
        form = FileConfigForm(request.POST)
        if form.is_valid():
            file_config = form.save(commit=False)
            file_config.client = client
            file_config.save()
            messages.success(request, 'File configuration created successfully.')
            return redirect('file_config_list', client_id=client.id)
    else:
        form = FileConfigForm()
    return render(request, 'client_manager/file_config_form.html', {'form': form, 'client': client, 'title': 'Create File Configuration'})

@login_required
def file_config_update(request, pk):
    file_config = get_object_or_404(FileConfig, pk=pk)
    if request.method == 'POST':
        form = FileConfigForm(request.POST, instance=file_config)
        if form.is_valid():
            form.save()
            messages.success(request, 'File configuration updated successfully.')
            return redirect('file_config_list', client_id=file_config.client.id)
    else:
        form = FileConfigForm(instance=file_config)
    return render(request, 'client_manager/file_config_form.html', {'form': form, 'client': file_config.client, 'title': 'Update File Configuration'})

@login_required
def file_config_delete(request, pk):
    file_config = get_object_or_404(FileConfig, pk=pk)
    if request.method == 'POST':
        client_id = file_config.client.id
        file_config.delete()
        messages.success(request, 'File configuration deleted successfully.')
        return redirect('file_config_list', client_id=client_id)
    return render(request, 'client_manager/file_config_confirm_delete.html', {'file_config': file_config})

@login_required
def download_10pm_files(request):
    if request.method == 'POST':
        form = DownloadForm(request.POST)
        if form.is_valid():
            selected_date = form.cleaned_data['selected_date']
            selected_date_str = selected_date.strftime('%Y-%m-%d') if selected_date else None
            download_10pm_files_task.delay(selected_date=selected_date_str)
            messages.success(request, '10PM file download task has been triggered.')
            return redirect('downloaded_files')
    else:
        form = DownloadForm()
    return render(request, 'client_manager/download_10pm.html', {'form': form})

@login_required
def downloaded_files(request):
    downloaded_files = DownloadedFile.objects.all().order_by('-downloaded_at')
    return render(request, 'client_manager/downloaded_files.html', {'downloaded_files': downloaded_files})

@login_required
def view_file(request, file_id):
    downloaded_file = get_object_or_404(DownloadedFile, id=file_id)
    content_type, _ = mimetypes.guess_type(downloaded_file.original_filename)
    print(f"view_file - file_id: {file_id}, filename: {downloaded_file.original_filename}, content_type: {content_type}")
    if not content_type:
        content_type = 'application/octet-stream'
    
    logger.info(f"Guessed Content-Type for {downloaded_file.original_filename}: {content_type}")
    if downloaded_file.file_type.lower() == 'txt' and content_type != 'text/plain':
        logger.warning(f"Mismatch: file_type is 'txt' but Content-Type is {content_type}. Forcing text/plain.")
        content_type = 'text/plain'

    logger.info(f"Viewing file {downloaded_file.original_filename} with Content-Type: {content_type}")

    if content_type == 'text/plain':
        file_content = BytesIO(downloaded_file.file_content)
        response = FileResponse(file_content, content_type=content_type)
        response['Content-Disposition'] = f'inline; filename="{downloaded_file.original_filename}"'
        return response
    elif content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
        response = HttpResponse(downloaded_file.file_content, content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename="{downloaded_file.original_filename}"'
        return response
    else:
        response = HttpResponse(downloaded_file.file_content, content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename="{downloaded_file.original_filename}"'
        return response

@login_required
def replace_file(request, file_id):
    downloaded_file = get_object_or_404(DownloadedFile, id=file_id)
    if request.method == 'POST':
        if 'file' in request.FILES:
            new_file = request.FILES['file']
            file_content = new_file.read()
            downloaded_file.file_content = file_content
            downloaded_file.original_filename = new_file.name
            downloaded_file.file_type = os.path.splitext(new_file.name)[1].lstrip('.')
            downloaded_file.save()
            messages.success(request, "File replaced successfully.")
        else:
            messages.error(request, "No file uploaded.")
        return redirect('client_details', client_id=downloaded_file.client.id)
    return render(request, 'client_manager/replace_file.html', {'downloaded_file': downloaded_file})

@login_required
def delete_file(request, file_id):
    downloaded_file = get_object_or_404(DownloadedFile, id=file_id)
    client_id = downloaded_file.client.id
    if request.method == 'POST':
        downloaded_file.delete()
        messages.success(request, "File deleted successfully.")
        return redirect('client_details', client_id=client_id)
    return render(request, 'client_manager/confirm_delete.html', {
        'object': downloaded_file,
        'type': 'Downloaded File',
        'client': downloaded_file.client
    })

@csrf_exempt
@login_required
def send_to_sftp(request):
    if request.method != 'POST':
        return JsonResponse({"status": "error", "message": "Invalid request method."}, status=400)

    file_id = request.POST.get('file_id')
    client_id = request.POST.get('client_id')

    try:
        downloaded_file = DownloadedFile.objects.get(id=file_id)
        client = Client.objects.get(id=client_id)

        if not downloaded_file.is_validated:
            return JsonResponse({"status": "error", "message": "File has validation errors and cannot be sent."}, status=400)

        if downloaded_file.sent_to_sftp:
            return JsonResponse({"status": "error", "message": "File has already been sent to SFTP."}, status=400)

        if not (client.sftp_host and client.sftp_username and client.sftp_password):
            return JsonResponse({"status": "error", "message": "SFTP credentials are missing for this client."}, status=400)

        # Write the file content to a temporary file
        temp_file_path = f"/tmp/{downloaded_file.original_filename}"
        with open(temp_file_path, 'wb') as f:
            f.write(downloaded_file.file_content)

        # Establish SFTP connection
        transport = paramiko.Transport((client.sftp_host, client.sftp_port or 22))
        transport.connect(username=client.sftp_username, password=client.sftp_password)
        sftp = paramiko.SFTPClient.from_transport(transport)

        # Upload the file
        remote_path = f"/{client.name}/{downloaded_file.original_filename}"
        with open(temp_file_path, 'rb') as local_file:
            sftp.putfo(local_file, remote_path)
        logger.info(f"File {downloaded_file.original_filename} sent to SFTP server at {remote_path}")

        # Mark as sent
        downloaded_file.sent_to_sftp = True
        downloaded_file.save()

        # Clean up
        sftp.close()
        transport.close()
        os.remove(temp_file_path)

        return JsonResponse({"status": "success", "message": "File sent to SFTP successfully."})
    except Exception as e:
        logger.error(f"Error sending file {file_id} to SFTP: {str(e)}", exc_info=True)
        # Store the SFTP error in validation_errors if it fails
        try:
            downloaded_file.validation_errors = f"SFTP transfer failed: {str(e)}"
            downloaded_file.save()
        except:
            pass
        return JsonResponse({"status": "error", "message": f"Error: {str(e)}"}, status=500)

@login_required
def upload_config_view(request, client_id):
    client = Client.objects.get(id=client_id)
    if request.method == "POST":
        form = UploadConfigForm(request.POST)
        if form.is_valid():
            upload_config = form.save(commit=False)
            upload_config.client = client
            upload_config.save()
            messages.success(request, "Upload configuration saved successfully.")
            return redirect('client_detail', client_id=client_id)
    else:
        form = UploadConfigForm(initial={'client': client})
    return render(request, 'client_manager/upload_config.html', {'form': form, 'client': client})