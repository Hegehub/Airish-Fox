# Generated manually for Airish Fox payments stage 6.

import decimal
import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = [
        ("orders", "0002_order_manual_review"),
    ]
    operations = [
        migrations.CreateModel(
            name="PaymentTransaction",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("provider", models.CharField(default="antom_2c2p", max_length=40, verbose_name="Провайдер")),
                ("payment_request_id", models.CharField(max_length=120, unique=True, verbose_name="Payment request ID")),
                ("provider_payment_id", models.CharField(blank=True, max_length=120, verbose_name="Provider payment ID")),
                ("amount", models.DecimalField(decimal_places=2, max_digits=14, validators=[django.core.validators.MinValueValidator(decimal.Decimal("0"))], verbose_name="Сумма")),
                ("currency", models.CharField(default="VND", max_length=3, verbose_name="Валюта")),
                ("status", models.CharField(choices=[("created", "Created"), ("pending", "Pending"), ("redirected", "Redirected"), ("paid", "Paid"), ("failed", "Failed"), ("cancelled", "Cancelled"), ("expired", "Expired"), ("refunded", "Refunded")], db_index=True, default="created", max_length=20, verbose_name="Статус")),
                ("checkout_url", models.URLField(blank=True, verbose_name="Checkout URL")),
                ("raw_request", models.JSONField(blank=True, default=dict, verbose_name="Raw request")),
                ("raw_response", models.JSONField(blank=True, default=dict, verbose_name="Raw response")),
                ("error_code", models.CharField(blank=True, max_length=120, verbose_name="Код ошибки")),
                ("error_message", models.TextField(blank=True, verbose_name="Ошибка")),
                ("idempotency_key", models.CharField(blank=True, max_length=160, null=True, unique=True, verbose_name="Idempotency key")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Создана")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Обновлена")),
                ("paid_at", models.DateTimeField(blank=True, null=True, verbose_name="Оплачена")),
                ("failed_at", models.DateTimeField(blank=True, null=True, verbose_name="Ошибка оплаты")),
                ("order", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="payment_transactions", to="orders.order", verbose_name="Заказ")),
            ],
            options={"verbose_name": "Платёжная транзакция", "verbose_name_plural": "Платёжные транзакции", "ordering": ["-created_at"], "indexes": [models.Index(fields=["provider", "payment_request_id"], name="payments_pa_provider_5b85e7_idx"), models.Index(fields=["order", "status"], name="payments_pa_order_i_6ddae8_idx"), models.Index(fields=["created_at"], name="payments_pa_created_4619af_idx")]},
        ),
        migrations.CreateModel(
            name="PaymentWebhookEvent",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("provider", models.CharField(default="antom_2c2p", max_length=40, verbose_name="Провайдер")),
                ("event_id", models.CharField(blank=True, max_length=120, verbose_name="Event ID")),
                ("payment_request_id", models.CharField(blank=True, max_length=120, verbose_name="Payment request ID")),
                ("headers", models.JSONField(default=dict, verbose_name="Headers")),
                ("payload", models.JSONField(default=dict, verbose_name="Payload")),
                ("raw_body", models.TextField(blank=True, verbose_name="Raw body")),
                ("signature_valid", models.BooleanField(default=False, verbose_name="Signature valid")),
                ("processed", models.BooleanField(default=False, verbose_name="Processed")),
                ("processing_error", models.TextField(blank=True, verbose_name="Processing error")),
                ("received_at", models.DateTimeField(auto_now_add=True, verbose_name="Received")),
                ("processed_at", models.DateTimeField(blank=True, null=True, verbose_name="Processed at")),
            ],
            options={"verbose_name": "Webhook оплаты", "verbose_name_plural": "Webhooks оплаты", "ordering": ["-received_at"], "indexes": [models.Index(fields=["provider", "payment_request_id"], name="payments_pa_provider_2e2c36_idx"), models.Index(fields=["processed"], name="payments_pa_process_58deab_idx"), models.Index(fields=["received_at"], name="payments_pa_receive_c53506_idx")]},
        ),
        migrations.CreateModel(
            name="PaymentStatusHistory",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("old_status", models.CharField(blank=True, max_length=40, verbose_name="Старый статус")),
                ("new_status", models.CharField(max_length=40, verbose_name="Новый статус")),
                ("reason", models.TextField(blank=True, verbose_name="Причина")),
                ("raw_payload", models.JSONField(blank=True, default=dict, verbose_name="Payload")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Создан")),
                ("transaction", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="status_history", to="payments.paymenttransaction", verbose_name="Транзакция")),
            ],
            options={"verbose_name": "История статуса оплаты", "verbose_name_plural": "История статусов оплаты", "ordering": ["-created_at"]},
        ),
    ]
