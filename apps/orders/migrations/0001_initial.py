# Generated manually for Airish Fox checkout stage 5.

import apps.orders.models
import decimal
import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("promotions", "0001_initial"),
        ("shipping", "0001_initial"),
    ]
    operations = [
        migrations.CreateModel(
            name="Order",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("number", models.CharField(db_index=True, default=apps.orders.models.generate_order_number, max_length=32, unique=True, verbose_name="Номер")),
                ("email", models.EmailField(max_length=254, verbose_name="Email")),
                ("phone", models.CharField(max_length=40, verbose_name="Телефон")),
                ("full_name", models.CharField(max_length=160, verbose_name="Имя")),
                ("shipping_country", models.CharField(default="Vietnam", max_length=80, verbose_name="Страна")),
                ("shipping_city", models.CharField(max_length=120, verbose_name="Город")),
                ("shipping_district", models.CharField(blank=True, max_length=120, verbose_name="Район")),
                ("shipping_street_address", models.TextField(verbose_name="Адрес")),
                ("shipping_postal_code", models.CharField(blank=True, max_length=30, verbose_name="Почтовый индекс")),
                ("shipping_method_name", models.CharField(blank=True, max_length=120, verbose_name="Название доставки")),
                ("status", models.CharField(choices=[("draft", "Draft"), ("pending_payment", "Pending payment"), ("paid", "Paid"), ("processing", "Processing"), ("shipped", "Shipped"), ("completed", "Completed"), ("cancelled", "Cancelled"), ("refunded", "Refunded")], db_index=True, default="draft", max_length=40, verbose_name="Статус")),
                ("payment_status", models.CharField(choices=[("unpaid", "Unpaid"), ("pending", "Pending"), ("paid", "Paid"), ("failed", "Failed"), ("refunded", "Refunded")], db_index=True, default="unpaid", max_length=40, verbose_name="Статус оплаты")),
                ("currency", models.CharField(default="VND", max_length=3, verbose_name="Валюта")),
                ("subtotal", models.DecimalField(decimal_places=2, default=0, max_digits=14, validators=[django.core.validators.MinValueValidator(decimal.Decimal("0"))], verbose_name="Subtotal")),
                ("discount_total", models.DecimalField(decimal_places=2, default=0, max_digits=14, validators=[django.core.validators.MinValueValidator(decimal.Decimal("0"))], verbose_name="Скидка")),
                ("shipping_total", models.DecimalField(decimal_places=2, default=0, max_digits=14, validators=[django.core.validators.MinValueValidator(decimal.Decimal("0"))], verbose_name="Доставка")),
                ("grand_total", models.DecimalField(decimal_places=2, default=0, max_digits=14, validators=[django.core.validators.MinValueValidator(decimal.Decimal("0"))], verbose_name="Итого")),
                ("promo_code_snapshot", models.CharField(blank=True, max_length=50, verbose_name="Промокод snapshot")),
                ("is_gift", models.BooleanField(default=False, verbose_name="Подарок")),
                ("gift_wrap", models.BooleanField(default=False, verbose_name="Подарочная упаковка")),
                ("gift_message", models.TextField(blank=True, verbose_name="Подарочное сообщение")),
                ("hide_price_in_package", models.BooleanField(default=False, verbose_name="Скрыть цены")),
                ("notes", models.TextField(blank=True, verbose_name="Комментарий")),
                ("customer_ip", models.GenericIPAddressField(blank=True, null=True, verbose_name="IP")),
                ("user_agent", models.TextField(blank=True, verbose_name="User agent")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Создан")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Обновлён")),
                ("promo_code", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="orders", to="promotions.promocode", verbose_name="Промокод")),
                ("shipping_method", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="orders", to="shipping.shippingmethod", verbose_name="Способ доставки")),
                ("user", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="orders", to=settings.AUTH_USER_MODEL, verbose_name="Пользователь")),
            ],
            options={"verbose_name": "Заказ", "verbose_name_plural": "Заказы", "ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="OrderItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("product_id_snapshot", models.PositiveIntegerField(blank=True, null=True, verbose_name="Product ID")),
                ("variant_id_snapshot", models.PositiveIntegerField(blank=True, null=True, verbose_name="Variant ID")),
                ("product_name", models.CharField(max_length=180, verbose_name="Товар")),
                ("variant_sku", models.CharField(max_length=100, verbose_name="SKU")),
                ("size", models.CharField(blank=True, max_length=80, verbose_name="Размер")),
                ("color_name", models.CharField(blank=True, max_length=80, verbose_name="Цвет")),
                ("color_hex", models.CharField(blank=True, max_length=7, verbose_name="HEX")),
                ("quantity", models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name="Количество")),
                ("unit_price", models.DecimalField(decimal_places=2, max_digits=14, validators=[django.core.validators.MinValueValidator(decimal.Decimal("0"))], verbose_name="Цена")),
                ("line_total", models.DecimalField(decimal_places=2, max_digits=14, validators=[django.core.validators.MinValueValidator(decimal.Decimal("0"))], verbose_name="Сумма")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Создан")),
                ("order", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="items", to="orders.order", verbose_name="Заказ")),
            ],
            options={"verbose_name": "Позиция заказа", "verbose_name_plural": "Позиции заказа", "ordering": ["created_at"]},
        ),
        migrations.CreateModel(
            name="OrderStatusHistory",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("old_status", models.CharField(blank=True, max_length=40, verbose_name="Старый статус")),
                ("new_status", models.CharField(max_length=40, verbose_name="Новый статус")),
                ("comment", models.TextField(blank=True, verbose_name="Комментарий")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Создан")),
                ("order", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="status_history", to="orders.order", verbose_name="Заказ")),
            ],
            options={"verbose_name": "История статуса", "verbose_name_plural": "История статусов", "ordering": ["-created_at"]},
        ),
    ]
