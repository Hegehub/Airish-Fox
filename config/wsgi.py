"""WSGI config for Airish Fox."""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.prod")

application = get_wsgi_application()

# Vercel's Python runtime expects a top-level ASGI/WSGI callable named `app`.
app = application
