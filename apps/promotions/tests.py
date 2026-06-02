"""Promotion tests."""

from decimal import Decimal
from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from .models import PromoCode


class PromoCodeTests(TestCase):
    def test_percent_promo_works(self):
        promo = PromoCode.objects.create(code="MINT10", discount_type=PromoCode.DiscountType.PERCENT, value=Decimal("10"))
        self.assertEqual(promo.calculate_discount(Decimal("1000.00")), Decimal("100.00"))

    def test_fixed_promo_works(self):
        promo = PromoCode.objects.create(code="FIXED", discount_type=PromoCode.DiscountType.FIXED, value=Decimal("150.00"))
        self.assertEqual(promo.calculate_discount(Decimal("1000.00")), Decimal("150.00"))

    def test_expired_promo_does_not_work(self):
        promo = PromoCode.objects.create(code="OLD", discount_type=PromoCode.DiscountType.FIXED, value=Decimal("150.00"), valid_until=timezone.now() - timedelta(days=1))
        self.assertFalse(promo.is_valid_now())
        self.assertEqual(promo.calculate_discount(Decimal("1000.00")), Decimal("0.00"))

    def test_inactive_promo_does_not_work(self):
        promo = PromoCode.objects.create(code="OFF", discount_type=PromoCode.DiscountType.FIXED, value=Decimal("150.00"), is_active=False)
        self.assertFalse(promo.is_valid_now())

    def test_discount_not_more_than_subtotal(self):
        promo = PromoCode.objects.create(code="BIG", discount_type=PromoCode.DiscountType.FIXED, value=Decimal("9999.00"))
        self.assertEqual(promo.calculate_discount(Decimal("500.00")), Decimal("500.00"))
