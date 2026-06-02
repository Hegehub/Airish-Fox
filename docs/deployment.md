# Deployment guide

## Production settings

Use `DJANGO_SETTINGS_MODULE=config.settings.prod`. Provide `SECRET_KEY`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, `DATABASE_URL`, `REDIS_URL` and a non-default `ADMIN_URL`.

## Static files

WhiteNoise is configured for compressed manifest static files. Run:

```bash
python manage.py collectstatic --noinput
```

## Database

Run migrations before starting web workers:

```bash
python manage.py migrate
```

## Runtime command

```bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

## Celery

Redis is used as broker/result backend. Start a worker with:

```bash
celery -A config worker -l info
```

Email and reconciliation tasks are placeholder-safe and must not block checkout or payment webhook handling.

## Docker notes

Do not copy `.env` into the image. Provide environment variables at runtime. Keep Antom and Google credentials separate between sandbox and live environments.
