# client_manager/admin.py
from django.contrib import admin
from .models import Client, Path, Task, OutputConfig, FileConfig, DownloadedFile

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'sftp_host', 'is_active', 'created_at', 'updated_at')  # Removed 'description'
    list_filter = ('is_active',)
    search_fields = ('name', 'sftp_host')
    fields = ('name', 'sftp_host', 'sftp_username', 'sftp_password', 'sftp_port', 'is_active')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Path)
class PathAdmin(admin.ModelAdmin):
    list_display = ('client', 'path', 'max_files')
    list_filter = ('client',)
    search_fields = ('path',)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(OutputConfig)
class OutputConfigAdmin(admin.ModelAdmin):
    list_display = ('client', 'path', 'task', 'file_type', 'output_dir', 'filename_template')
    list_filter = ('client', 'task', 'file_type')
    search_fields = ('output_dir', 'filename_template')

@admin.register(FileConfig)
class FileConfigAdmin(admin.ModelAdmin):
    list_display = ('client', 'file_type', 'remote_path', 'is_active', 'created_at', 'updated_at')
    list_filter = ('file_type', 'is_active')
    search_fields = ('client__name', 'remote_path')

@admin.register(DownloadedFile)
class DownloadedFileAdmin(admin.ModelAdmin):
    list_display = ('client', 'original_filename', 'file_type', 'is_validated', 'downloaded_at')
    list_filter = ('is_validated', 'file_type')
    search_fields = ('original_filename', 'client__name')