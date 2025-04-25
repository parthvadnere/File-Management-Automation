# client_manager/models.py
from django.db import models

class Client(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    sftp_host = models.CharField(max_length=255, blank=True, null=True)
    sftp_username = models.CharField(max_length=100, blank=True, null=True)
    sftp_password = models.CharField(max_length=100, blank=True, null=True)
    sftp_port = models.IntegerField(default=22, blank=True, null=True)

    def __str__(self):
        return self.name

class Path(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='paths')
    path = models.CharField(max_length=255)
    file_types = models.JSONField()
    max_files = models.IntegerField(default=3)
    file_pattern = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.client.name} - {self.path}"

class Task(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class OutputConfig(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='output_configs')
    path = models.ForeignKey(Path, on_delete=models.CASCADE, related_name='output_configs')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='output_configs')
    file_type = models.CharField(max_length=10)
    output_dir = models.CharField(max_length=255)
    filename_template = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.client.name} - {self.path.path} - {self.task.name} - {self.file_type}"

class DownloadedFile(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='downloaded_files')
    file = models.FileField(upload_to='downloads/%Y/%m/%d/')
    original_filename = models.CharField(max_length=255)
    file_type = models.CharField(max_length=10)
    downloaded_at = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=255)  # The Pharmpix path (e.g., ALLIED/Claims)

    def __str__(self):
        return f"{self.original_filename} - {self.client.name}"