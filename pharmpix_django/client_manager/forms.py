# client_manager/forms.py
from django import forms
from .models import Client, Path, Task, OutputConfig

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'description', 'sftp_host', 'sftp_username', 'sftp_password', 'sftp_port']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'sftp_password': forms.PasswordInput(),
        }

class PathForm(forms.ModelForm):
    class Meta:
        model = Path
        fields = ['client', 'path', 'file_types', 'max_files', 'file_pattern']
        widgets = {
            'file_types': forms.TextInput(attrs={'placeholder': 'e.g., [".txt", ".xlsx"]'}),
        }

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class OutputConfigForm(forms.ModelForm):
    class Meta:
        model = OutputConfig
        fields = ['client', 'path', 'task', 'file_type', 'output_dir', 'filename_template']