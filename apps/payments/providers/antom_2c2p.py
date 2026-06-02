"""Antom / 2C2P hosted payment provider."""

from __future__ import annotations

import json
import logging
from decimal import Decimal
from urllib.parse import urlparse

from django.conf import settings
from django.utils import timezone

from apps.orders.models import Order

from ..exceptions import PaymentConfigurationError, PaymentProviderError, PaymentSignatureError
from ..models import PaymentStatusHistory, PaymentTransaction, PaymentWebhookEvent
from ..services import get_or_create_payment_transaction, mark_transaction_failed, mark_transaction_paid
from .base import PaymentProvider
from .signing import parse_signature_header, sign_request, verify_signature

logger = logging.getLogger("payments")


SUCCESS_STATUSES = {"SUCCESS", "PAYMENT_SUCCESS", "PAID", "S"}
FAILED_STATUSES = {"FAIL", "FAILED", "PAYMENT_FAILED", "F"}
CANCELLED_STATUSES = {"CANCELLED", "CANCELED", "CANCEL"}
EXPIRED_STATUSES = {"EXPIRED", "TIMEOUT"}
PENDING_STATUSES = {"PENDING", "PROCESSING", "U"}


def format_amount_for_antom(amount, currency):
    """Format amount for Antom.

    Public Antom docs state some APIs expect amount in the smallest currency
    unit. VND has no minor unit, so we keep integer VND here. Verify the exact
    amount format for the contracted Antom product before live launch.
    """
    value = Decimal(amount)
    if currency.upper() in {"VND", "JPY", "KRW"}:
        return str(int(value))
    return str(int((value * Decimal("100")).quantize(Decimal("1"))))


def map_antom_status_to_internal(payload):
    """Map Antom payment status payload to internal transaction status.

    TODO: verify status mapping against live Antom API response examples before
    production go-live.
    """
    raw_status = (
        payload.get("paymentStatus")
        or payload.get("paymentResultCode")
        or payload.get("result", {}).get("resultStatus")
        or payload.get("result", {}).get("resultCode")
        or ""
    ).upper()
    if raw_status in SUCCESS_STATUSES:
        return PaymentTransaction.Status.PAID
    if raw_status in FAILED_STATUSES:
        return PaymentTransaction.Status.FAILED
    if raw_status in CANCELLED_STATUSES:
        return PaymentTransaction.Status.CANCELLED
    if raw_status in EXPIRED_STATUSES:
        return PaymentTransaction.Status.EXPIRED
    if raw_status in PENDING_STATUSES:
        return PaymentTransaction.Status.PENDING
    return PaymentTransaction.Status.PENDING


class Antom2C2PPaymentProvider(PaymentProvider):
    provider_name = "antom_2c2p"
    api_path = "/ams/api/v1/payments/pay"

    @property
    def config(self):
        return settings.ANTOM

    def _require_config(self):
        required = ["GATEWAY_URL", "CLIENT_ID", "MERCHANT_PRIVATE_KEY", "PUBLIC_KEY", "KEY_VERSION"]
        missing = [key for key in required if not self.config.get(key)]
        if missing:
            raise PaymentConfigurationError(f"Antom settings missing: {', '.join(missing)}")

    def create_payment(self, order):
        self._require_config()
        transaction_obj = get_or_create_payment_transaction(order)
        if transaction_obj.status == PaymentTransaction.Status.PAID:
            raise PaymentProviderError("Этот заказ уже оплачен.")
        if transaction_obj.checkout_url and transaction_obj.status in {PaymentTransaction.Status.REDIRECTED, PaymentTransaction.Status.PENDING}:
            return transaction_obj

        payload = self.build_payment_payload(order, transaction_obj.payment_request_id)
        transaction_obj.raw_request = payload
        transaction_obj.status = PaymentTransaction.Status.PENDING
        transaction_obj.save(update_fields=["raw_request", "status", "updated_at"])
        response = self.send_payment_request(payload)
        checkout_url = self.extract_checkout_url(response)
        if not checkout_url:
            transaction_obj.status = PaymentTransaction.Status.FAILED
            transaction_obj.raw_response = response
            transaction_obj.error_code = response.get("result", {}).get("resultCode", "")
            transaction_obj.error_message = response.get("result", {}).get("resultMessage", "No checkout URL returned")
            transaction_obj.failed_at = timezone.now()
            transaction_obj.save(update_fields=["status", "raw_response", "error_code", "error_message", "failed_at", "updated_at"])
            raise PaymentProviderError(transaction_obj.error_message or "Antom не вернул URL оплаты.")

        old_status = transaction_obj.status
        transaction_obj.checkout_url = checkout_url
        transaction_obj.raw_response = response
        transaction_obj.status = PaymentTransaction.Status.REDIRECTED
        transaction_obj.save(update_fields=["checkout_url", "raw_response", "status", "updated_at"])
        PaymentStatusHistory.objects.create(transaction=transaction_obj, old_status=old_status, new_status=transaction_obj.status, reason="created hosted checkout", raw_payload=response)
        return transaction_obj

    def build_payment_payload(self, order, payment_request_id):
        amount = {"currency": order.currency, "value": format_amount_for_antom(order.grand_total, order.currency)}
        return {
            "productCode": "CASHIER_PAYMENT",
            "paymentRequestId": payment_request_id,
            "paymentAmount": amount,
            "paymentRedirectUrl": self.config["RETURN_URL"],
            "paymentNotifyUrl": self.config["NOTIFY_URL"],
            "env": {"terminalType": "WEB"},
            "order": {
                "referenceOrderId": order.number,
                "orderDescription": f"Airish Fox order {order.number}",
                "orderAmount": amount,
            },
        }

    def send_payment_request(self, payload):
        import requests

        body = json.dumps(payload, separators=(",", ":"), ensure_ascii=False)
        request_time = str(int(timezone.now().timestamp() * 1000))
        uri_path = urlparse(self.config["GATEWAY_URL"]).path or self.api_path
        signature = sign_request(self.config["MERCHANT_PRIVATE_KEY"], "POST", uri_path, self.config["CLIENT_ID"], request_time, body)
        headers = {
            "Content-Type": "application/json",
            "Request-Time": request_time,
            "client-id": self.config["CLIENT_ID"],
            "Signature": f"algorithm=RSA256,keyVersion={self.config['KEY_VERSION']},signature={signature}",
        }
        try:
            response = requests.post(self.config["GATEWAY_URL"], data=body.encode("utf-8"), headers=headers, timeout=self.config["TIMEOUT_SECONDS"])
            response.raise_for_status()
        except requests.RequestException as exc:
            logger.exception("Antom provider request failed")
            raise PaymentProviderError("Не удалось создать платёж у провайдера.") from exc
        return response.json()

    def extract_checkout_url(self, response):
        return (
            response.get("normalUrl")
            or response.get("paymentUrl")
            or response.get("checkoutUrl")
            or response.get("redirectUrl")
            or response.get("paymentSessionData", {}).get("paymentUrl")
        )

    def parse_return(self, request):
        payment_request_id = request.GET.get("paymentRequestId") or request.GET.get("payment_request_id")
        if payment_request_id:
            return PaymentTransaction.objects.filter(payment_request_id=payment_request_id).select_related("order").first()
        order_number = request.GET.get("orderNumber") or request.GET.get("referenceOrderId")
        if order_number:
            return PaymentTransaction.objects.filter(order__number=order_number).select_related("order").order_by("-created_at").first()
        return None

    def verify_notification(self, request) -> dict:
        raw_body = request.body.decode("utf-8")
        signature_header = request.headers.get("Signature", "")
        request_time = request.headers.get("Request-Time", "")
        client_id = request.headers.get("client-id", self.config.get("CLIENT_ID", ""))
        parts = parse_signature_header(signature_header)
        if parts.key_version and self.config.get("KEY_VERSION") and parts.key_version != self.config["KEY_VERSION"]:
            raise PaymentSignatureError("Unexpected key version.")
        valid = verify_signature(
            self.config["PUBLIC_KEY"],
            parts.signature,
            "POST",
            request.path,
            client_id,
            request_time,
            raw_body,
        )
        if not valid:
            raise PaymentSignatureError("Invalid Antom signature.")
        return json.loads(raw_body or "{}")

    def handle_notification(self, webhook_event: PaymentWebhookEvent):
        payload = webhook_event.payload
        payment_request_id = webhook_event.payment_request_id or payload.get("paymentRequestId")
        transaction_obj = PaymentTransaction.objects.select_related("order").filter(payment_request_id=payment_request_id).first()
        if not transaction_obj:
            webhook_event.processing_error = "Unknown payment_request_id."
            webhook_event.save(update_fields=["processing_error"])
            logger.warning("Unknown payment_request_id webhook", extra={"payment_request_id": payment_request_id})
            return None

        internal_status = map_antom_status_to_internal(payload)
        if internal_status == PaymentTransaction.Status.PAID:
            return mark_transaction_paid(transaction_obj, payload)
        if internal_status in {PaymentTransaction.Status.FAILED, PaymentTransaction.Status.CANCELLED, PaymentTransaction.Status.EXPIRED}:
            return mark_transaction_failed(transaction_obj, payload, reason=f"Antom status {internal_status}")

        old_status = transaction_obj.status
        transaction_obj.status = internal_status
        transaction_obj.raw_response = payload
        transaction_obj.provider_payment_id = payload.get("paymentId", transaction_obj.provider_payment_id)
        transaction_obj.save(update_fields=["status", "raw_response", "provider_payment_id", "updated_at"])
        PaymentStatusHistory.objects.create(transaction=transaction_obj, old_status=old_status, new_status=internal_status, reason="Antom pending webhook", raw_payload=payload)
        return transaction_obj
