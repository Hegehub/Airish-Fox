# Generated manually for Airish Fox cart stage 4.

import decimal
import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("catalog", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Cart",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("session_key", models.CharField(blank=True, db_index=True, max_length=80, null=True, verbose_name="Session key")),
                ("status", models.CharField(choices=[("active", "Active"), ("converted", "Converted"), ("abandoned", "Abandoned")], db_index=True, default="active", max_length=20, verbose_name="Статус")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Создана")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Обновлена")),
                ("user", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name="carts", to=settings.AUTH_USER_MODEL, verbose_name="Пользователь")),
            ],
            options={"verbose_name": "Корзина", "verbose_name_plural": "Корзины", "ordering": ["-updated_at"]},
        ),
        migrations.CreateModel(
            name="CartItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("quantity", models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name="Количество")),
                ("unit_price_snapshot", models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(decimal.Decimal("0"))], verbose_name="Цена при добавлении")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Создан")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Обновлён")),
                ("cart", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="items", to="cart.cart", verbose_name="Корзина")),
                ("variant", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="cart_items", to="catalog.productvariant", verbose_name="Вариант товара")),
            ],
            options={"verbose_name": "Позиция корзины", "verbose_name_plural": "Позиции корзины", "ordering": ["created_at"]},
        ),
        migrations.AddConstraint(
            model_name="cartitem",
            constraint=models.UniqueConstraint(fields=("cart", "variant"), name="cart_unique_variant_per_cart"),
        ),
        migrations.AddConstraint(
            model_name="cartitem",
            constraint=models.CheckConstraint(condition=models.Q(quantity__gte=1), name="cart_item_quantity_gte_1"),
        ),
        migrations.AddConstraint(
            model_name="cartitem",
            constraint=models.CheckConstraint(condition=models.Q(unit_price_snapshot__gte=0), name="cart_item_unit_price_gte_0"),
        ),
    ]
