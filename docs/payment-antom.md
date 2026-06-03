# Payments: 2C2P by Antom

Airish Fox uses a hosted/redirect Antom payment flow. Customers leave the site for the protected provider checkout page; the Django app never receives card number, CVV or expiry data.

## Environment variables

Configure these in sandbox first:

- `ANTOM_ENV=sandbox`
- `ANTOM_GATEWAY_URL`
- `ANTOM_CLIENT_ID`
- `ANTOM_MERCHANT_PRIVATE_KEY`
- `ANTOM_PUBLIC_KEY`
- `ANTOM_KEY_VERSION`
- `ANTOM_PAYMENT_CURRENCY=VND`
- `ANTOM_NOTIFY_URL=https://your-domain/payments/antom/notify/`
- `ANTOM_RETURN_URL=https://your-domain/payments/antom/return/`

## Webhook safety

`/payments/antom/notify/` stores raw webhook payloads in `PaymentWebhookEvent`, verifies signatures, and only then updates `PaymentTransaction`/`Order`. Invalid signatures do not update orders. Duplicate webhooks are idempotent and must not reduce stock twice.

## Reconciliation

Run:

```bash
python manage.py reconcile_payments --dry-run
```

This lists stale pending transactions for manual/provider reconciliation. Live provider status polling is intentionally left as a TODO until production Antom API response contracts and credentials are confirmed.

## Go-live checklist

- Confirm amount formatting for VND with Antom.
- Confirm status mapping against live/sandbox response examples.
- Confirm signature content and notification response format.
- Use public HTTPS notify/return URLs.
- Restrict logs and rotate keys if credentials leak.

## Return URL vs notification URL

The browser return URL is only a UX signal. It must never mark an order paid by itself. The notification/webhook endpoint is the source of truth after signature verification.

## Testing cards

Use only Antom sandbox testing instruments documented in the merchant dashboard or official sandbox documentation. Do not add card-number fields to Airish Fox templates.
