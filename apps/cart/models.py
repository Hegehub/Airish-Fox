"""Cart models for guest and authenticated customer carts."""

from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from apps.catalog.models import ProductVariant


class Cart(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        CONVERTED = "converted", "Converted"
        ABANDONED = "abandoned", "Abandoned"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="carts",
        verbose_name="Пользователь",
        blank=True,
        null=True,
    )
    session_key = models.CharField("Session key", max_length=80, blank=True, null=True, db_index=True)
    status = models.CharField("Статус", max_length=20, choices=Status.choices, default=Status.ACTIVE, db_index=True)
    created_at = models.DateTimeField("Создана", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлена", auto_now=True)

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"
        ordering = ["-updated_at"]

    def __str__(self):
        owner = self.user.get_username() if self.user_id else self.session_key
        return f"Cart #{self.pk} ({owner or 'anonymous'})"

    def get_subtotal(self):
        return sum((item.get_line_total() for item in self.items.select_related("variant")), Decimal("0.00"))

    def get_items_count(self):
        return sum(item.quantity for item in self.items.all())

    def is_empty(self):
        return not self.items.exists()


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items", verbose_name="Корзина")
    variant = models.ForeignKey(ProductVariant, on_delete=models.PROTECT, related_name="cart_items", verbose_name="Вариант товара")
    quantity = models.PositiveIntegerField("Количество", validators=[MinValueValidator(1)])
    unit_price_snapshot = models.DecimalField("Цена при добавлении", max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal("0"))])
    created_at = models.DateTimeField("Создан", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлён", auto_now=True)

    class Meta:
        verbose_name = "Позиция корзины"
        verbose_name_plural = "Позиции корзины"
        ordering = ["created_at"]
        constraints = [
            models.UniqueConstraint(fields=["cart", "variant"], name="cart_unique_variant_per_cart"),
            models.CheckConstraint(condition=models.Q(quantity__gte=1), name="cart_item_quantity_gte_1"),
            models.CheckConstraint(condition=models.Q(unit_price_snapshot__gte=0), name="cart_item_unit_price_gte_0"),
        ]

    def __str__(self):
        return f"{self.variant} × {self.quantity}"

    def get_line_total(self):
        return self.unit_price_snapshot * self.quantity
