"""Promotion models for checkout discounts."""

from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


class PromoCode(models.Model):
    class DiscountType(models.TextChoices):
        PERCENT = "percent", "Percent"
        FIXED = "fixed", "Fixed"

    code = models.CharField("Код", max_length=50, unique=True)
    description = models.CharField("Описание", max_length=255, blank=True)
    discount_type = models.CharField("Тип скидки", max_length=20, choices=DiscountType.choices)
    value = models.DecimalField("Значение", max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal("0"))])
    is_active = models.BooleanField("Активен", default=True)
    valid_from = models.DateTimeField("Действует с", null=True, blank=True)
    valid_until = models.DateTimeField("Действует до", null=True, blank=True)
    max_uses = models.PositiveIntegerField("Максимум использований", null=True, blank=True)
    used_count = models.PositiveIntegerField("Использований", default=0)
    minimum_order_amount = models.DecimalField("Минимальная сумма", max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(Decimal("0"))])
    created_at = models.DateTimeField("Создан", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлён", auto_now=True)

    class Meta:
        verbose_name = "Промокод"
        verbose_name_plural = "Промокоды"
        ordering = ["code"]

    def __str__(self):
        return self.code

    def clean(self):
        if self.discount_type == self.DiscountType.PERCENT and self.value > 100:
            raise ValidationError({"value": "Процентная скидка не может быть больше 100%."})

    def save(self, *args, **kwargs):
        self.code = self.code.strip().upper()
        self.full_clean()
        super().save(*args, **kwargs)

    def is_valid_now(self):
        now = timezone.now()
        if not self.is_active:
            return False
        if self.valid_from and self.valid_from > now:
            return False
        if self.valid_until and self.valid_until < now:
            return False
        if self.max_uses is not None and self.used_count >= self.max_uses:
            return False
        return True

    def can_apply_to_amount(self, amount):
        return self.is_valid_now() and amount >= self.minimum_order_amount

    def calculate_discount(self, amount):
        amount = Decimal(amount)
        if not self.can_apply_to_amount(amount):
            return Decimal("0.00")
        if self.discount_type == self.DiscountType.PERCENT:
            discount = amount * (self.value / Decimal("100"))
        else:
            discount = self.value
        return min(discount.quantize(Decimal("0.01")), amount)
