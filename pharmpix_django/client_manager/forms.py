# client_manager/forms.py
from django import forms
from .models import Client, Path, Task, OutputConfig, FileConfig, UploadConfig
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label="Email",
        max_length=254,
        help_text="Required. Enter a valid email address (e.g., user@example.com).",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')
        widgets = {
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['password1'].help_text = (
            "Required. Your password must contain at least 8 characters, including one uppercase letter, "
            "one lowercase letter, one number, and one special character (e.g., !@#$%)."
        )
        self.fields['password2'].help_text = "Required. Please re-enter your password for confirmation."

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")
        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        if not any(char.isupper() for char in password1):
            raise ValidationError("Password must contain at least one uppercase letter.")
        if not any(char.islower() for char in password1):
            raise ValidationError("Password must contain at least one lowercase letter.")
        if not any(char.isdigit() for char in password1):
            raise ValidationError("Password must contain at least one number.")
        if not any(char in '!@#$%^&*()_+-=[]{}|;:,.<>?`~' for char in password1):
            raise ValidationError("Password must contain at least one special character.")
        return password1

    # def clean_password2(self):
    #     password1 = self.cleaned_data.get('password1')
    #     password2 = self.cleaned_data.get('password2')
    #     if password1 and password2 and password1 == password2:
    #         # Additional check to detect if password2 was copied from password1
    #         if self.data.get('password1') == self.data.get('password2'):
    #             raise ValidationError("Please type the confirm password manually; copying is not allowed.")
    #     return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
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


class UploadConfigForm(forms.ModelForm):
    class Meta:
        model = UploadConfig
        fields = ['upload_endpoint', 'token']