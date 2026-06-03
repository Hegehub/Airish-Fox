"""Order models for checkout without payment gateway integration."""

from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone

from apps.promotions.models import PromoCode
from apps.shipping.models import ShippingMethod


def generate_order_number():
    """Generate a unique human-readable order number."""
    today = timezone.localdate()
    prefix = f"AF-{today:%Y%m%d}"
    count = Order.objects.filter(created_at__date=today).count() + 1
    for offset in range(100):
        number = f"{prefix}-{count + offset:06d}"
        if not Order.objects.filter(number=number).exists():
            return number
    fallback = timezone.now().strftime("%H%M%S%f")[-10:]
    return f"{prefix}-{fallback}"


class Order(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PENDING_PAYMENT = "pending_payment", "Pending payment"
        PAID = "paid", "Paid"
        PROCESSING = "processing", "Processing"
        SHIPPED = "shipped", "Shipped"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"
        REFUNDED = "refunded", "Refunded"

    class PaymentStatus(models.TextChoices):
        UNPAID = "unpaid", "Unpaid"
        PENDING = "pending", "Pending"
        PAID = "paid", "Paid"
        FAILED = "failed", "Failed"
        REFUNDED = "refunded", "Refunded"

    number = models.CharField("Номер", max_length=32, unique=True, db_index=True, default=generate_order_number)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="orders", verbose_name="Пользователь")
    email = models.EmailField("Email")
    phone = models.CharField("Телефон", max_length=40)
    full_name = models.CharField("Имя", max_length=160)

    shipping_country = models.CharField("Страна", max_length=80, default="Vietnam")
    shipping_city = models.CharField("Город", max_length=120)
    shipping_district = models.CharField("Район", max_length=120, blank=True)
    shipping_street_address = models.TextField("Адрес")
    shipping_postal_code = models.CharField("Почтовый индекс", max_length=30, blank=True)
    shipping_method = models.ForeignKey(ShippingMethod, null=True, blank=True, on_delete=models.SET_NULL, related_name="orders", verbose_name="Способ доставки")
    shipping_method_name = models.CharField("Название доставки", max_length=120, blank=True)
    pickup_store = models.ForeignKey("store_locator.StoreLocation", null=True, blank=True, on_delete=models.SET_NULL, related_name="pickup_orders", verbose_name="Магазин самовывоза")
    pickup_store_name = models.CharField("Магазин самовывоза snapshot", max_length=160, blank=True)
    pickup_store_address = models.TextField("Адрес самовывоза snapshot", blank=True)

    status = models.CharField("Статус", max_length=40, choices=Status.choices, default=Status.DRAFT, db_index=True)
    payment_status = models.CharField("Статус оплаты", max_length=40, choices=PaymentStatus.choices, default=PaymentStatus.UNPAID, db_index=True)

    currency = models.CharField("Валюта", max_length=3, default="VND")
    subtotal = models.DecimalField("Subtotal", max_digits=14, decimal_places=2, default=0, validators=[MinValueValidator(Decimal("0"))])
    discount_total = models.DecimalField("Скидка", max_digits=14, decimal_places=2, default=0, validators=[MinValueValidator(Decimal("0"))])
    shipping_total = models.DecimalField("Доставка", max_digits=14, decimal_places=2, default=0, validators=[MinValueValidator(Decimal("0"))])
    grand_total = models.DecimalField("Итого", max_digits=14, decimal_places=2, default=0, validators=[MinValueValidator(Decimal("0"))])

    promo_code = models.ForeignKey(PromoCode, null=True, blank=True, on_delete=models.SET_NULL, related_name="orders", verbose_name="Промокод")
    promo_code_snapshot = models.CharField("Промокод snapshot", max_length=50, blank=True)

    is_gift = models.BooleanField("Подарок", default=False)
    gift_wrap = models.BooleanField("Подарочная упаковка", default=False)
    gift_message = models.TextField("Подарочное сообщение", blank=True)
    hide_price_in_package = models.BooleanField("Скрыть цены", default=False)

    notes = models.TextField("Комментарий", blank=True)
    requires_manual_review = models.BooleanField("Требует ручной проверки", default=False)
    manual_review_reason = models.TextField("Причина ручной проверки", blank=True)
    customer_ip = models.GenericIPAddressField("IP", null=True, blank=True)
    user_agent = models.TextField("User agent", blank=True)
    created_at = models.DateTimeField("Создан", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлён", auto_now=True)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ["-created_at"]

    def __str__(self):
        return self.number

    def recalculate_totals(self, save=True):
        subtotal = sum((item.line_total for item in self.items.all()), Decimal("0.00"))
        self.subtotal = subtotal
        self.discount_total = min(self.discount_total, subtotal)
        self.grand_total = max(subtotal - self.discount_total + self.shipping_total, Decimal("0.00"))
        if save:
            self.save(update_fields=["subtotal", "discount_total", "shipping_total", "grand_total", "updated_at"])
        return self.grand_total

    def can_be_paid(self):
        return self.status == self.Status.PENDING_PAYMENT and self.payment_status in {self.PaymentStatus.UNPAID, self.PaymentStatus.PENDING, self.PaymentStatus.FAILED}

    def mark_pending_payment(self, comment="Заказ создан и ожидает оплаты."):
        old_status = self.status
        self.status = self.Status.PENDING_PAYMENT
        self.payment_status = self.PaymentStatus.UNPAID
        self.save(update_fields=["status", "payment_status", "updated_at"])
        OrderStatusHistory.objects.create(order=self, old_status=old_status, new_status=self.status, comment=comment)

    def get_absolute_url(self):
        return reverse("orders:detail", kwargs={"number": self.number})


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE, verbose_name="Заказ")
    product_id_snapshot = models.PositiveIntegerField("Product ID", null=True, blank=True)
    variant_id_snapshot = models.PositiveIntegerField("Variant ID", null=True, blank=True)
    product_name = models.CharField("Товар", max_length=180)
    variant_sku = models.CharField("SKU", max_length=100)
    size = models.CharField("Размер", max_length=80, blank=True)
    color_name = models.CharField("Цвет", max_length=80, blank=True)
    color_hex = models.CharField("HEX", max_length=7, blank=True)
    quantity = models.PositiveIntegerField("Количество", validators=[MinValueValidator(1)])
    unit_price = models.DecimalField("Цена", max_digits=14, decimal_places=2, validators=[MinValueValidator(Decimal("0"))])
    line_total = models.DecimalField("Сумма", max_digits=14, decimal_places=2, validators=[MinValueValidator(Decimal("0"))])
    created_at = models.DateTimeField("Создан", auto_now_add=True)

    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказа"
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.product_name} × {self.quantity}"


class OrderStatusHistory(models.Model):
    order = models.ForeignKey(Order, related_name="status_history", on_delete=models.CASCADE, verbose_name="Заказ")
    old_status = models.CharField("Старый статус", max_length=40, blank=True)
    new_status = models.CharField("Новый статус", max_length=40)
    comment = models.TextField("Комментарий", blank=True)
    created_at = models.DateTimeField("Создан", auto_now_add=True)

    class Meta:
        verbose_name = "История статуса"
        verbose_name_plural = "История статусов"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.order.number}: {self.old_status} → {self.new_status}"
