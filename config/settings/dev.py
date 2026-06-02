"""Development settings for Airish Fox."""

from .base import *  # noqa: F403

DEBUG = env_bool("DEBUG", True)  # noqa: F405
SECRET_KEY = os.getenv("SECRET_KEY", SECRET_KEY)  # noqa: F405
ALLOWED_HOSTS = env_list("ALLOWED_HOSTS", ["127.0.0.1", "localhost"])  # noqa: F405
DATABASES = {"default": database_config("sqlite:///db.sqlite3")}  # noqa: F405
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
