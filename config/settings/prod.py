"""Production settings for Airish Fox."""

from django.core.exceptions import ImproperlyConfigured

from .base import *  # noqa: F403

DEBUG = False

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ImproperlyConfigured("SECRET_KEY is required in production.")

ALLOWED_HOSTS = env_list("ALLOWED_HOSTS")  # noqa: F405
if not ALLOWED_HOSTS:
    raise ImproperlyConfigured("ALLOWED_HOSTS is required in production.")

if not os.getenv("ADMIN_URL") or ADMIN_URL == "admin/":
    raise ImproperlyConfigured("ADMIN_URL must be set to a non-default path in production.")

CSRF_TRUSTED_ORIGINS = env_list("CSRF_TRUSTED_ORIGINS")  # noqa: F405
DATABASES = {"default": database_config()}  # noqa: F405

SECURE_SSL_REDIRECT = env_bool("SECURE_SSL_REDIRECT", True)  # noqa: F405
SESSION_COOKIE_SECURE = env_bool("SESSION_COOKIE_SECURE", True)  # noqa: F405
CSRF_COOKIE_SECURE = env_bool("CSRF_COOKIE_SECURE", True)  # noqa: F405
SECURE_HSTS_SECONDS = int(os.getenv("SECURE_HSTS_SECONDS", "31536000"))
SECURE_HSTS_INCLUDE_SUBDOMAINS = env_bool("SECURE_HSTS_INCLUDE_SUBDOMAINS", True)  # noqa: F405
SECURE_HSTS_PRELOAD = env_bool("SECURE_HSTS_PRELOAD", False)  # noqa: F405


if env_bool("ANTOM_PAYMENTS_ENABLED", False):  # noqa: F405
    required_antom_keys = ["GATEWAY_URL", "CLIENT_ID", "MERCHANT_PRIVATE_KEY", "PUBLIC_KEY", "KEY_VERSION"]
    missing_antom_keys = [key for key in required_antom_keys if not ANTOM.get(key)]  # noqa: F405
    if missing_antom_keys:
        raise ImproperlyConfigured(f"Missing Antom payment settings: {', '.join(missing_antom_keys)}")
