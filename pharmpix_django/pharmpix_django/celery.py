# pharmpix_django/celery.py
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pharmpix_django.settings')

app = Celery('pharmpix_django')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.beat_schedule = {
    'run-10pm-files-task': {
        'task': 'client_manager.tasks.download_10pm_files_task',
        'schedule': crontab(hour=22, minute=0),  # Runs daily at 10 PM
    },
}