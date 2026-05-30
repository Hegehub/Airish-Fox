from .base import *  # noqa: F403

DEBUG = True
SECRET_KEY = os.getenv('SECRET_KEY', SECRET_KEY)  # noqa: F405
ALLOWED_HOSTS = env_list('ALLOWED_HOSTS', '127.0.0.1,localhost')  # noqa: F405
DATABASES = {'default': database_from_url(default_sqlite=True)}  # noqa: F405
