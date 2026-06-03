"""Payment tests for Antom / 2C2P hosted flow."""

import json
from decimal import Decimal
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.urls import reverse

from apps.catalog.models import Category, Product, ProductVariant
from apps.orders.models import Order
from apps.payments.exceptions import PaymentSignatureError
from apps.payments.models import PaymentTransaction, PaymentWebhookEvent
from apps.shipping.models import ShippingMethod


TEST_ANTOM = {
    "ENV": "sandbox",
    "GATEWAY_URL": "https://example.test/ams/api/v1/payments/pay",
    "CLIENT_ID": "client-id",
    "MERCHANT_PRIVATE_KEY": "test-private-key",
    "PUBLIC_KEY": "test-public-key",
    "KEY_VERSION": "1",
    "PAYMENT_CURRENCY": "VND",
    "NOTIFY_URL": "http://testserver/payments/antom/notify/",
    "RETURN_URL": "http://testserver/payments/antom/return/",
    "TIMEOUT_SECONDS": 20,
}


class PaymentTestDataMixin:
    def setUp(self):
        self.user = User.objects.create_user(username="payfox", email="pay@example.com", password="StrongPass123")
        self.other_user = User.objects.create_user(username="otherpay", email="otherpay@example.com", password="StrongPass123")
        self.staff = User.objects.create_user(username="staffpay", email="staff@example.com", password="StrongPass123", is_staff=True)
        self.shipping = ShippingMethod.objects.create(name="Standard", code="standard", base_price=Decimal("0.00"))
        self.category = Category.objects.create(name="Pay", slug="pay")
        self.product = Product.objects.create(name="Pay Dress", slug="pay-dress", category=self.category, short_description="Pay")
        self.variant = ProductVariant.objects.create(product=self.product, sku="PAY-S", size="S", color_name="Mint", price=Decimal("1000.00"), stock_quantity=5)
        self.order = Order.objects.create(
            user=self.user,
            email="pay@example.com",
            phone="1",
            full_name="Pay Fox",
            shipping_city="HCMC",
            shipping_street_address="Street",
            shipping_method=self.shipping,
            shipping_method_name=self.shipping.name,
            subtotal=Decimal("2000.00"),
            grand_total=Decimal("2000.00"),
            status=Order.Status.PENDING_PAYMENT,
            payment_status=Order.PaymentStatus.UNPAID,
        )
        self.order.items.create(product_id_snapshot=self.product.id, variant_id_snapshot=self.variant.id, product_name=self.product.name, variant_sku=self.variant.sku, size=self.variant.size, color_name=self.variant.color_name, color_hex=self.variant.color_hex, quantity=2, unit_price=Decimal("1000.00"), line_total=Decimal("2000.00"))


@override_settings(ANTOM=TEST_ANTOM)
class PaymentTests(PaymentTestDataMixin, TestCase):
    @patch("apps.payments.providers.antom_2c2p.Antom2C2PPaymentProvider.send_payment_request")
    def test_create_payment_transaction_for_order(self, mock_send):
        mock_send.return_value = {"normalUrl": "https://pay.example/checkout"}
        self.client.login(username="payfox", password="StrongPass123")
        response = self.client.post(reverse("payments:antom_create", kwargs={"order_number": self.order.number}))
        self.assertEqual(response.status_code, 302)
        transaction = PaymentTransaction.objects.get(order=self.order)
        self.assertEqual(transaction.status, PaymentTransaction.Status.REDIRECTED)

    @patch("apps.payments.providers.antom_2c2p.Antom2C2PPaymentProvider.send_payment_request")
    def test_cannot_create_payment_for_paid_order(self, mock_send):
        self.order.status = Order.Status.PROCESSING
        self.order.payment_status = Order.PaymentStatus.PAID
        self.order.save(update_fields=["status", "payment_status"])
        self.client.login(username="payfox", password="StrongPass123")
        response = self.client.post(reverse("payments:antom_create", kwargs={"order_number": self.order.number}))
        self.assertEqual(response.status_code, 200)
        mock_send.assert_not_called()

    @patch("apps.payments.providers.antom_2c2p.Antom2C2PPaymentProvider.send_payment_request")
    def test_payment_request_id_is_idempotent(self, mock_send):
        mock_send.return_value = {"normalUrl": "https://pay.example/checkout"}
        self.client.login(username="payfox", password="StrongPass123")
        url = reverse("payments:antom_create", kwargs={"order_number": self.order.number})
        self.client.post(url)
        self.client.post(url)
        self.assertEqual(PaymentTransaction.objects.filter(order=self.order).count(), 1)

    @patch("apps.payments.providers.antom_2c2p.Antom2C2PPaymentProvider.verify_notification")
    def test_webhook_invalid_signature_does_not_update_order(self, mock_verify):
        mock_verify.side_effect = PaymentSignatureError("invalid")
        payload = {"paymentRequestId": "PAY-UNKNOWN", "paymentStatus": "SUCCESS"}
        response = self.client.post(reverse("payments:antom_notify"), data=json.dumps(payload), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.order.refresh_from_db()
        self.assertEqual(self.order.payment_status, Order.PaymentStatus.UNPAID)

    @patch("apps.payments.providers.antom_2c2p.Antom2C2PPaymentProvider.verify_notification")
    def test_webhook_valid_signature_marks_order_paid(self, mock_verify):
        transaction = PaymentTransaction.objects.create(order=self.order, payment_request_id=f"PAY-{self.order.number}", amount=self.order.grand_total, currency="VND")
        payload = {"paymentRequestId": transaction.payment_request_id, "paymentStatus": "SUCCESS", "paymentId": "provider-1"}
        mock_verify.return_value = payload
        response = self.client.post(reverse("payments:antom_notify"), data=json.dumps(payload), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.order.refresh_from_db()
        transaction.refresh_from_db()
        self.assertEqual(self.order.payment_status, Order.PaymentStatus.PAID)
        self.assertEqual(transaction.status, PaymentTransaction.Status.PAID)

    @patch("apps.payments.providers.antom_2c2p.Antom2C2PPaymentProvider.verify_notification")
    def test_duplicate_webhook_does_not_reduce_stock_twice(self, mock_verify):
        transaction = PaymentTransaction.objects.create(order=self.order, payment_request_id=f"PAY-{self.order.number}", amount=self.order.grand_total, currency="VND")
        payload = {"paymentRequestId": transaction.payment_request_id, "paymentStatus": "SUCCESS"}
        mock_verify.return_value = payload
        url = reverse("payments:antom_notify")
        self.client.post(url, data=json.dumps(payload), content_type="application/json")
        self.client.post(url, data=json.dumps(payload), content_type="application/json")
        self.variant.refresh_from_db()
        self.assertEqual(self.variant.stock_quantity, 3)

    @patch("apps.payments.providers.antom_2c2p.Antom2C2PPaymentProvider.verify_notification")
    def test_unknown_payment_request_id_webhook_is_stored(self, mock_verify):
        payload = {"paymentRequestId": "PAY-MISSING", "paymentStatus": "SUCCESS"}
        mock_verify.return_value = payload
        response = self.client.post(reverse("payments:antom_notify"), data=json.dumps(payload), content_type="application/json")
        self.assertEqual(response.status_code, 202)
        event = PaymentWebhookEvent.objects.get(payment_request_id="PAY-MISSING")
        self.assertIn("Unknown", event.processing_error)

    def test_return_url_does_not_mark_paid_without_webhook(self):
        transaction = PaymentTransaction.objects.create(order=self.order, payment_request_id=f"PAY-{self.order.number}", amount=self.order.grand_total, currency="VND", status=PaymentTransaction.Status.REDIRECTED)
        response = self.client.get(reverse("payments:antom_return"), {"paymentRequestId": transaction.payment_request_id})
        self.assertEqual(response.status_code, 200)
        self.order.refresh_from_db()
        self.assertEqual(self.order.payment_status, Order.PaymentStatus.UNPAID)

    def test_payment_create_requires_order_owner(self):
        self.client.login(username="otherpay", password="StrongPass123")
        response = self.client.post(reverse("payments:antom_create", kwargs={"order_number": self.order.number}))
        self.assertEqual(response.status_code, 404)

    @patch("apps.payments.providers.antom_2c2p.Antom2C2PPaymentProvider.send_payment_request")
    def test_staff_can_process_payment(self, mock_send):
        mock_send.return_value = {"normalUrl": "https://pay.example/checkout"}
        self.client.login(username="staffpay", password="StrongPass123")
        response = self.client.post(reverse("payments:antom_create", kwargs={"order_number": self.order.number}))
        self.assertEqual(response.status_code, 302)

    @patch("apps.payments.providers.antom_2c2p.Antom2C2PPaymentProvider.verify_notification")
    def test_failed_payment_does_not_reduce_stock(self, mock_verify):
        transaction = PaymentTransaction.objects.create(order=self.order, payment_request_id=f"PAY-{self.order.number}", amount=self.order.grand_total, currency="VND")
        payload = {"paymentRequestId": transaction.payment_request_id, "paymentStatus": "FAIL", "result": {"resultCode": "FAIL", "resultMessage": "declined"}}
        mock_verify.return_value = payload
        response = self.client.post(reverse("payments:antom_notify"), data=json.dumps(payload), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.variant.refresh_from_db()
        self.order.refresh_from_db()
        self.assertEqual(self.variant.stock_quantity, 5)
        self.assertEqual(self.order.payment_status, Order.PaymentStatus.FAILED)
