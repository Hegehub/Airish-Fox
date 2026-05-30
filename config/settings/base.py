import os
from pathlib import Path
from urllib.parse import urlparse

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / '.env')


def env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.lower() in {'1', 'true', 'yes', 'on'}


def env_int(name: str, default: int = 0) -> int:
    value = os.getenv(name)
    if value is None or value == '':
        return default
    return int(value)


def env_list(name: str, default: str = '') -> list[str]:
    return [item.strip() for item in os.getenv(name, default).split(',') if item.strip()]


def env_path(name: str, default: Path) -> Path:
    value = os.getenv(name)
    path = Path(value) if value else Path(default)
    return path if path.is_absolute() else BASE_DIR / path


def database_from_url(default_sqlite: bool = True) -> dict:
    database_url = os.getenv('DATABASE_URL')
    if not database_url and default_sqlite:
        database_url = f'sqlite:///{BASE_DIR / "db.sqlite3"}'
    if not database_url:
        raise RuntimeError('DATABASE_URL is required for this environment')

    parsed = urlparse(database_url)
    if parsed.scheme in {'postgres', 'postgresql'}:
        return {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': parsed.path.lstrip('/'),
            'USER': parsed.username or '',
            'PASSWORD': parsed.password or '',
            'HOST': parsed.hostname or '',
            'PORT': parsed.port or '',
            'CONN_MAX_AGE': env_int('DB_CONN_MAX_AGE', 60),
        }
    if parsed.scheme == 'sqlite':
        db_path = parsed.path or str(BASE_DIR / 'db.sqlite3')
        if db_path != ':memory:' and not db_path.startswith(str(BASE_DIR)):
            db_path = str(BASE_DIR / db_path.lstrip('/'))
        return {'ENGINE': 'django.db.backends.sqlite3', 'NAME': db_path}
    raise RuntimeError(f'Unsupported DATABASE_URL scheme: {parsed.scheme}')


SECRET_KEY = os.getenv('SECRET_KEY', 'dev-airish-fox-secret-key')
DEBUG = env_bool('DEBUG', False)
ALLOWED_HOSTS = env_list('ALLOWED_HOSTS', '127.0.0.1,localhost')
CSRF_TRUSTED_ORIGINS = env_list('CSRF_TRUSTED_ORIGINS')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'apps.core',
    'apps.catalog',
    'apps.reviews',
    'apps.contacts',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.core.context_processors.site_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'

DATABASES = {'default': database_from_url()}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = os.getenv('TIME_ZONE', 'Europe/Moscow')
USE_I18N = True
USE_TZ = True

STATIC_URL = os.getenv('STATIC_URL', 'static/')
STATIC_ROOT = env_path('STATIC_ROOT', BASE_DIR / 'staticfiles')
STATICFILES_DIRS = [BASE_DIR / 'static']
MEDIA_URL = os.getenv('MEDIA_URL', 'media/')
MEDIA_ROOT = env_path('MEDIA_ROOT', BASE_DIR / 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')

SECURE_SSL_REDIRECT = env_bool('SECURE_SSL_REDIRECT', False)
SESSION_COOKIE_SECURE = env_bool('SESSION_COOKIE_SECURE', False)
CSRF_COOKIE_SECURE = env_bool('CSRF_COOKIE_SECURE', False)
SECURE_HSTS_SECONDS = env_int('SECURE_HSTS_SECONDS', 0)
SECURE_HSTS_INCLUDE_SUBDOMAINS = env_bool('SECURE_HSTS_INCLUDE_SUBDOMAINS', False)
SECURE_HSTS_PRELOAD = env_bool('SECURE_HSTS_PRELOAD', False)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
X_FRAME_OPTIONS = 'DENY'

CONTACT_RATE_LIMIT_SECONDS = env_int('CONTACT_RATE_LIMIT_SECONDS', 30)
SITE_SETTINGS_CACHE_TIMEOUT = env_int('SITE_SETTINGS_CACHE_TIMEOUT', 300)
