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

## Recommended infrastructure

Use Docker-based hosting on a VPS, Render, Railway, Fly.io or another platform that supports long-running Django web workers, PostgreSQL, Redis, public HTTPS webhooks and persistent/static/media strategy. Vercel is not an ideal primary host for this full Django e-commerce app because media uploads, background workers and payment webhooks require a server-oriented deployment model.

## Reverse proxy and HTTPS

Terminate HTTPS at a trusted proxy and forward `X-Forwarded-Proto=https`. In production set `SECURE_PROXY_SSL_HEADER_ENABLED=True`, keep secure cookies enabled and configure `ALLOWED_HOSTS`/`CSRF_TRUSTED_ORIGINS` for the public domain.

## Media storage

Local `MEDIA_ROOT` is acceptable for development. Production should use S3-compatible object storage or another durable media backend, with private credentials supplied via environment variables and no uploaded media committed to git.

## Backups and rollback

- Back up PostgreSQL before deployments and before destructive migrations.
- Keep database dumps and media backups in a separate secured location.
- Roll back by redeploying the previous image and restoring the database only if the migration plan requires it.
- Keep Antom sandbox/live credentials separate and rotate secrets if exposure is suspected.
