"""Payment models for hosted Antom / 2C2P payment flow."""

from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

from apps.orders.models import Order


class PaymentTransaction(models.Model):
    class Status(models.TextChoices):
        CREATED = "created", "Created"
        PENDING = "pending", "Pending"
        REDIRECTED = "redirected", "Redirected"
        PAID = "paid", "Paid"
        FAILED = "failed", "Failed"
        CANCELLED = "cancelled", "Cancelled"
        EXPIRED = "expired", "Expired"
        REFUNDED = "refunded", "Refunded"

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="payment_transactions", verbose_name="Заказ")
    provider = models.CharField("Провайдер", max_length=40, default="antom_2c2p")
    payment_request_id = models.CharField("Payment request ID", max_length=120, unique=True)
    provider_payment_id = models.CharField("Provider payment ID", max_length=120, blank=True)
    amount = models.DecimalField("Сумма", max_digits=14, decimal_places=2, validators=[MinValueValidator(Decimal("0"))])
    currency = models.CharField("Валюта", max_length=3, default="VND")
    status = models.CharField("Статус", max_length=20, choices=Status.choices, default=Status.CREATED, db_index=True)
    checkout_url = models.URLField("Checkout URL", blank=True)
    raw_request = models.JSONField("Raw request", default=dict, blank=True)
    raw_response = models.JSONField("Raw response", default=dict, blank=True)
    error_code = models.CharField("Код ошибки", max_length=120, blank=True)
    error_message = models.TextField("Ошибка", blank=True)
    idempotency_key = models.CharField("Idempotency key", max_length=160, unique=True, blank=True, null=True)
    created_at = models.DateTimeField("Создана", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлена", auto_now=True)
    paid_at = models.DateTimeField("Оплачена", null=True, blank=True)
    failed_at = models.DateTimeField("Ошибка оплаты", null=True, blank=True)

    class Meta:
        verbose_name = "Платёжная транзакция"
        verbose_name_plural = "Платёжные транзакции"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["provider", "payment_request_id"]),
            models.Index(fields=["order", "status"]),
            models.Index(fields=["status"], name="payments_tx_status_idx"),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"{self.provider}:{self.payment_request_id}"

    def mark_status(self, status, save=True):
        self.status = status
        if status == self.Status.PAID and not self.paid_at:
            self.paid_at = timezone.now()
        if status in {self.Status.FAILED, self.Status.CANCELLED, self.Status.EXPIRED} and not self.failed_at:
            self.failed_at = timezone.now()
        if save:
            self.save(update_fields=["status", "paid_at", "failed_at", "updated_at"])


class PaymentWebhookEvent(models.Model):
    provider = models.CharField("Провайдер", max_length=40, default="antom_2c2p")
    event_id = models.CharField("Event ID", max_length=120, blank=True)
    payment_request_id = models.CharField("Payment request ID", max_length=120, blank=True)
    headers = models.JSONField("Headers", default=dict)
    payload = models.JSONField("Payload", default=dict)
    raw_body = models.TextField("Raw body", blank=True)
    signature_valid = models.BooleanField("Signature valid", default=False)
    processed = models.BooleanField("Processed", default=False)
    processing_error = models.TextField("Processing error", blank=True)
    received_at = models.DateTimeField("Received", auto_now_add=True)
    processed_at = models.DateTimeField("Processed at", null=True, blank=True)

    class Meta:
        verbose_name = "Webhook оплаты"
        verbose_name_plural = "Webhooks оплаты"
        ordering = ["-received_at"]
        indexes = [
            models.Index(fields=["provider", "payment_request_id"]),
            models.Index(fields=["processed"]),
            models.Index(fields=["received_at"]),
        ]

    def __str__(self):
        return f"{self.provider}:{self.payment_request_id or self.event_id or self.pk}"


class PaymentStatusHistory(models.Model):
    transaction = models.ForeignKey(PaymentTransaction, on_delete=models.CASCADE, related_name="status_history", verbose_name="Транзакция")
    old_status = models.CharField("Старый статус", max_length=40, blank=True)
    new_status = models.CharField("Новый статус", max_length=40)
    reason = models.TextField("Причина", blank=True)
    raw_payload = models.JSONField("Payload", default=dict, blank=True)
    created_at = models.DateTimeField("Создан", auto_now_add=True)

    class Meta:
        verbose_name = "История статуса оплаты"
        verbose_name_plural = "История статусов оплаты"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.transaction.payment_request_id}: {self.old_status} → {self.new_status}"
