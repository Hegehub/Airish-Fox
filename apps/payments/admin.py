"""Admin for payment models."""

from django.contrib import admin

from .models import PaymentStatusHistory, PaymentTransaction, PaymentWebhookEvent


class PaymentStatusHistoryInline(admin.TabularInline):
    model = PaymentStatusHistory
    extra = 0
    can_delete = False
    readonly_fields = ("old_status", "new_status", "reason", "raw_payload", "created_at")


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    inlines = (PaymentStatusHistoryInline,)
    list_display = ("order", "provider", "payment_request_id", "amount", "currency", "status", "created_at", "paid_at")
    list_filter = ("provider", "status", "currency", "created_at")
    search_fields = ("payment_request_id", "provider_payment_id", "order__number")
    readonly_fields = ("order", "provider", "payment_request_id", "provider_payment_id", "amount", "currency", "status", "checkout_url", "raw_request", "raw_response", "error_code", "error_message", "idempotency_key", "created_at", "updated_at", "paid_at", "failed_at")


@admin.register(PaymentWebhookEvent)
class PaymentWebhookEventAdmin(admin.ModelAdmin):
    list_display = ("provider", "payment_request_id", "signature_valid", "processed", "received_at")
    list_filter = ("provider", "signature_valid", "processed", "received_at")
    search_fields = ("payment_request_id", "event_id")
    readonly_fields = ("provider", "event_id", "payment_request_id", "headers", "payload", "raw_body", "signature_valid", "processed", "processing_error", "received_at", "processed_at")


@admin.register(PaymentStatusHistory)
class PaymentStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ("transaction", "old_status", "new_status", "created_at")
    search_fields = ("transaction__payment_request_id", "reason")
    readonly_fields = ("transaction", "old_status", "new_status", "reason", "raw_payload", "created_at")
