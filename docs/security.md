# Security checklist

Airish Fox production runs with `config.settings.prod`.

## Required environment

- `SECRET_KEY` must come from the runtime environment and must never be committed.
- `ALLOWED_HOSTS` must be explicit.
- `CSRF_TRUSTED_ORIGINS` must include public HTTPS origins that submit forms.
- `ADMIN_URL` must be set to a non-default path such as `secure-admin/`.
- HTTPS settings (`SECURE_SSL_REDIRECT`, secure cookies, HSTS) should remain enabled in production.

## Forms and abuse protection

Login, registration, checkout submission and payment creation use cache-backed rate limits configured with `RATE_LIMIT_*` variables. Checkout includes a hidden honeypot field; if it is filled, order creation is rejected without storing an order.

## Payments

The site uses hosted/redirect payment flow only. It must not collect, log or store PAN, CVV or expiry dates. Antom private/public keys are environment variables and must not be visible in admin or logs.

## Logging

Payment logs may include `payment_request_id`, order number and status transitions. Do not log private keys, customer passwords, authorization headers, card data or sensitive tokens.

## Reverse proxy

When running behind Nginx, Caddy, Traefik or a platform load balancer, set `SECURE_PROXY_SSL_HEADER_ENABLED=True` only if the proxy reliably sends `X-Forwarded-Proto=https`. Keep `USE_X_FORWARDED_HOST=True` only for trusted proxies.

## Email

Production SMTP credentials (`EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `DEFAULT_FROM_EMAIL`) must come from the runtime environment. Development can use Django's console backend.
