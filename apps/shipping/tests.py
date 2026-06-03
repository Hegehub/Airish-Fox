"""Shipping tests."""

from decimal import Decimal

from django.test import TestCase

from .models import ShippingMethod


class ShippingMethodTests(TestCase):
    def test_active_shipping_method(self):
        method = ShippingMethod.objects.create(name="Standard delivery", code="standard", base_price=Decimal("25000.00"))
        self.assertTrue(method.is_active)
        self.assertEqual(method.get_price_for_order(), Decimal("25000.00"))

    def test_inactive_method_not_available_for_checkout(self):
        ShippingMethod.objects.create(name="Inactive", code="inactive", base_price=Decimal("0.00"), is_active=False)
        self.assertFalse(ShippingMethod.objects.filter(is_active=True).exists())
