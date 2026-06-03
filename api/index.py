"""Vercel entrypoint for the Airish Fox Django application."""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.prod")

# Vercel Python runtime looks for a top-level WSGI/ASGI callable named `app`.
app = get_wsgi_application()
