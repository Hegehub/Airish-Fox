"""Order tests."""

from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from apps.orders.models import Order, OrderStatusHistory
from apps.shipping.models import ShippingMethod


class OrderTests(TestCase):
    def setUp(self):
        self.shipping = ShippingMethod.objects.create(name="Standard delivery", code="standard", base_price=Decimal("100.00"))
        self.user = User.objects.create_user(username="orderfox", email="order@example.com", password="StrongPass123")
        self.other_user = User.objects.create_user(username="otherorder", email="otherorder@example.com", password="StrongPass123")

    def create_order(self, user=None):
        return Order.objects.create(
            user=user,
            email="order@example.com",
            phone="1",
            full_name="Order Fox",
            shipping_city="HCMC",
            shipping_street_address="Street",
            shipping_method=self.shipping,
            shipping_method_name=self.shipping.name,
            subtotal=Decimal("1000.00"),
            shipping_total=Decimal("100.00"),
            grand_total=Decimal("1100.00"),
        )

    def test_order_number_unique(self):
        first = self.create_order()
        second = self.create_order()
        self.assertNotEqual(first.number, second.number)

    def test_order_detail_protected_from_other_users(self):
        order = self.create_order(user=self.user)
        self.client.login(username="otherorder", password="StrongPass123")
        response = self.client.get(order.get_absolute_url())
        self.assertEqual(response.status_code, 404)

    def test_status_history_created(self):
        order = self.create_order(user=self.user)
        order.mark_pending_payment()
        self.assertTrue(OrderStatusHistory.objects.filter(order=order, new_status=Order.Status.PENDING_PAYMENT).exists())
