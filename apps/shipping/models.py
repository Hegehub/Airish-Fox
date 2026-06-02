"""Shipping models for checkout delivery options."""

from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


class ShippingMethod(models.Model):
    name = models.CharField("Название", max_length=120)
    code = models.SlugField("Код", unique=True)
    description = models.TextField("Описание", blank=True)
    base_price = models.DecimalField("Базовая цена", max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal("0"))])
    is_active = models.BooleanField("Активен", default=True)
    sort_order = models.PositiveIntegerField("Порядок", default=0)
    created_at = models.DateTimeField("Создан", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлён", auto_now=True)

    class Meta:
        verbose_name = "Способ доставки"
        verbose_name_plural = "Способы доставки"
        ordering = ["sort_order", "base_price", "name"]

    def __str__(self):
        return self.name

    def get_price_for_order(self, order=None):
        return self.base_price

    @property
    def is_store_pickup(self):
        return self.code == "store-pickup"
