"""Celery application for background Airish Fox tasks."""

from __future__ import annotations

import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")

app = Celery("airish_fox")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
