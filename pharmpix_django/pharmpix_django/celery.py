# pharmpix_django/celery.py
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pharmpix_django.settings')

app = Celery('pharmpix_django')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()