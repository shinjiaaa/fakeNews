from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fakeNews.settings')

app = Celery('fakeNews')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()  # ← 태스크 자동 발견 추가!
