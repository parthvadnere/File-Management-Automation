# client_manager/forms.py
from django import forms
from .models import Client, Path, Task, OutputConfig, FileConfig, UploadConfig

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'sftp_host', 'sftp_username', 'sftp_password', 'sftp_port', 'is_active']
        widgets = {
            'sftp_password': forms.PasswordInput(),
        }

class PathForm(forms.ModelForm):
    class Meta:
        model = Path
        fields = ['client', 'path', 'file_types', 'max_files', 'file_pattern']
        widgets = {
            'file_types': forms.TextInput(attrs={'placeholder': 'e.g., [".txt", ".xlsx"]'}),
        }

class FileConfigForm(forms.ModelForm):
    class Meta:
        model = FileConfig
        fields = ['file_type', 'remote_path', 'file_pattern', 'local_path', 'renamed_pattern', 'is_active']

class DownloadForm(forms.Form):
    selected_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False,
        help_text="Select a date for downloading files (defaults to latest file/s if not specified)."
    )

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

class DownloadForm(forms.Form):
    selected_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False,
        help_text="Select a date for downloading files (defaults to latest file/s if not specified)."
    )
    task_type = forms.ChoiceField(choices=[('5PM', '5PM'), ('10PM', '10PM')], required=True)


class UploadConfigForm(forms.ModelForm):
    class Meta:
        model = UploadConfig
        fields = ['upload_endpoint', 'token']