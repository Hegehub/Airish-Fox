import os

from .base import *  # noqa: F403

DEBUG = env_bool('DEBUG', False)  # noqa: F405
SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY:
    raise RuntimeError('SECRET_KEY must be set in production')

ALLOWED_HOSTS = env_list('ALLOWED_HOSTS')  # noqa: F405
if not ALLOWED_HOSTS:
    raise RuntimeError('ALLOWED_HOSTS must be set in production')

DATABASES = {'default': database_from_url(default_sqlite=False)}  # noqa: F405
SECURE_SSL_REDIRECT = env_bool('SECURE_SSL_REDIRECT', True)  # noqa: F405
SESSION_COOKIE_SECURE = env_bool('SESSION_COOKIE_SECURE', True)  # noqa: F405
CSRF_COOKIE_SECURE = env_bool('CSRF_COOKIE_SECURE', True)  # noqa: F405
SECURE_HSTS_SECONDS = env_int('SECURE_HSTS_SECONDS', 31536000)  # noqa: F405
SECURE_HSTS_INCLUDE_SUBDOMAINS = env_bool('SECURE_HSTS_INCLUDE_SUBDOMAINS', True)  # noqa: F405
SECURE_HSTS_PRELOAD = env_bool('SECURE_HSTS_PRELOAD', True)  # noqa: F405
