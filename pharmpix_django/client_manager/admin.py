# client_manager/admin.py
from django.contrib import admin
from .models import Client, Path, Task, OutputConfig

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

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