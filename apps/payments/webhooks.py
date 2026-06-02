"""Webhook helpers for payment providers."""

import json

from django.utils import timezone

from .models import PaymentWebhookEvent
from .providers.antom_2c2p import Antom2C2PPaymentProvider


def extract_payment_request_id(payload):
    return payload.get("paymentRequestId") or payload.get("payment_request_id") or payload.get("payment", {}).get("paymentRequestId", "")


def extract_event_id(payload):
    return payload.get("eventId") or payload.get("notifyId") or payload.get("notificationId", "")


def build_notification_response(success=True, message="success"):
    """Build notification response; adapt here if Antom requires a different shape."""
    return {"result": {"resultStatus": "S" if success else "F", "resultMessage": message}}


def create_webhook_event_from_request(request, signature_valid=False, payload=None):
    raw_body = request.body.decode("utf-8")
    if payload is None:
        try:
            payload = json.loads(raw_body or "{}")
        except json.JSONDecodeError:
            payload = {}
    headers = {key: value for key, value in request.headers.items()}
    return PaymentWebhookEvent.objects.create(
        headers=headers,
        raw_body=raw_body,
        payload=payload,
        signature_valid=signature_valid,
        payment_request_id=extract_payment_request_id(payload),
        event_id=extract_event_id(payload),
    )


def process_antom_notification_event(event):
    provider = Antom2C2PPaymentProvider()
    provider.handle_notification(event)
    if not event.processing_error:
        event.processed = True
        event.processed_at = timezone.now()
        event.save(update_fields=["processed", "processed_at"])
    return event
