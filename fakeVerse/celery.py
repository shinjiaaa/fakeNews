# fakeNews/fakeNews/celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Django settings module 설정
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fakeVerse.settings")

app = Celery("fakeVerse")

# Django settings에서 Celery config 로드
app.config_from_object("django.conf:settings", namespace="CELERY")

# Celery task 자동 발견
app.autodiscover_tasks()
