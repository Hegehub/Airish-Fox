"""Base settings for Airish Fox."""

from __future__ import annotations

import os
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")


def env_bool(name: str, default: bool = False) -> bool:
    """Read a boolean value from environment variables."""
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def env_list(name: str, default: list[str] | None = None) -> list[str]:
    """Read a comma-separated list from environment variables."""
    value = os.getenv(name)
    if not value:
        return default or []
    return [item.strip() for item in value.split(",") if item.strip()]


def env_path(name: str, default: str) -> str:
    """Read a URL path from env and normalize it for Django path()."""
    value = os.getenv(name, default).strip().lstrip("/")
    return value if value.endswith("/") else f"{value}/"


def database_config(default: str = "sqlite:///db.sqlite3") -> dict[str, object]:
    """Build a Django database config from DATABASE_URL."""
    return dj_database_url.parse(
        os.getenv("DATABASE_URL", default),
        conn_max_age=int(os.getenv("DATABASE_CONN_MAX_AGE", "60")),
    )

SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-insecure-change-me")
DEBUG = env_bool("DEBUG", False)
ALLOWED_HOSTS = env_list("ALLOWED_HOSTS", ["127.0.0.1", "localhost"])
CSRF_TRUSTED_ORIGINS = env_list("CSRF_TRUSTED_ORIGINS")
ADMIN_URL = env_path("ADMIN_URL", "admin/")
APP_ENV = os.getenv("APP_ENV", "development")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "apps.core",
    "apps.catalog",
    "apps.accounts",
    "apps.cart",
    "apps.shipping",
    "apps.promotions",
    "apps.orders",
    "apps.checkout",
    "apps.payments",
    "apps.store_locator",
    "apps.brand",
    "apps.style_quiz",
    "apps.wishlist",
    "apps.drops",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "apps.core.context_processors.brand",
                "apps.cart.context_processors.cart_summary",
                "apps.store_locator.context_processors.store_context",
                "apps.wishlist.context_processors.wishlist_summary",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

DATABASES = {"default": database_config()}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "ru-ru"
TIME_ZONE = "Asia/Ho_Chi_Minh"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
REFERRER_POLICY = "strict-origin-when-cross-origin"
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "")
GOOGLE_MAPS_MAP_ID = os.getenv("GOOGLE_MAPS_MAP_ID", "")
GOOGLE_MAPS_DEFAULT_ZOOM = int(os.getenv("GOOGLE_MAPS_DEFAULT_ZOOM", "15"))

ANTOM = {
    "ENV": os.getenv("ANTOM_ENV", "sandbox"),
    "GATEWAY_URL": os.getenv("ANTOM_GATEWAY_URL", ""),
    "CLIENT_ID": os.getenv("ANTOM_CLIENT_ID", ""),
    "MERCHANT_PRIVATE_KEY": os.getenv("ANTOM_MERCHANT_PRIVATE_KEY", ""),
    "PUBLIC_KEY": os.getenv("ANTOM_PUBLIC_KEY", ""),
    "KEY_VERSION": os.getenv("ANTOM_KEY_VERSION", ""),
    "PAYMENT_CURRENCY": os.getenv("ANTOM_PAYMENT_CURRENCY", "VND"),
    "NOTIFY_URL": os.getenv("ANTOM_NOTIFY_URL", "http://localhost:8000/payments/antom/notify/"),
    "RETURN_URL": os.getenv("ANTOM_RETURN_URL", "http://localhost:8000/payments/antom/return/"),
    "TIMEOUT_SECONDS": int(os.getenv("ANTOM_TIMEOUT_SECONDS", "20")),
}

LOGIN_URL = "accounts:login"
LOGIN_REDIRECT_URL = "accounts:dashboard"
LOGOUT_REDIRECT_URL = "core:home"


# Lightweight anti-abuse limits. Values use "requests/window-seconds" format.
RATE_LIMITS = {
    "login": os.getenv("RATE_LIMIT_LOGIN", "10/300"),
    "register": os.getenv("RATE_LIMIT_REGISTER", "5/600"),
    "checkout": os.getenv("RATE_LIMIT_CHECKOUT", "8/300"),
    "payment_create": os.getenv("RATE_LIMIT_PAYMENT_CREATE", "12/300"),
}

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", REDIS_URL)
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", REDIS_URL)
CELERY_TASK_ALWAYS_EAGER = env_bool("CELERY_TASK_ALWAYS_EAGER", False)

SENTRY_DSN = os.getenv("SENTRY_DSN", "")
SENTRY_TRACES_SAMPLE_RATE = float(os.getenv("SENTRY_TRACES_SAMPLE_RATE", "0.0"))
if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        environment=APP_ENV,
        traces_sample_rate=SENTRY_TRACES_SAMPLE_RATE,
        send_default_pii=False,
    )

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "console": {"format": "%(asctime)s %(levelname)s %(name)s %(message)s"},
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "console"},
    },
    "loggers": {
        "django.request": {"handlers": ["console"], "level": os.getenv("DJANGO_REQUEST_LOG_LEVEL", "WARNING"), "propagate": True},
        "apps.payments": {"handlers": ["console"], "level": os.getenv("PAYMENTS_LOG_LEVEL", "INFO"), "propagate": False},
        "payments": {"handlers": ["console"], "level": os.getenv("PAYMENTS_LOG_LEVEL", "INFO"), "propagate": False},
        "apps.orders": {"handlers": ["console"], "level": "INFO", "propagate": False},
        "apps.checkout": {"handlers": ["console"], "level": "INFO", "propagate": False},
        "apps.cart": {"handlers": ["console"], "level": "INFO", "propagate": False},
    },
}
