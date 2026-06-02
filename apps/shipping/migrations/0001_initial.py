# Generated manually for Airish Fox checkout stage 5.

import decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="ShippingMethod",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120, verbose_name="Название")),
                ("code", models.SlugField(unique=True, verbose_name="Код")),
                ("description", models.TextField(blank=True, verbose_name="Описание")),
                ("base_price", models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(decimal.Decimal("0"))], verbose_name="Базовая цена")),
                ("is_active", models.BooleanField(default=True, verbose_name="Активен")),
                ("sort_order", models.PositiveIntegerField(default=0, verbose_name="Порядок")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Создан")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Обновлён")),
            ],
            options={"verbose_name": "Способ доставки", "verbose_name_plural": "Способы доставки", "ordering": ["sort_order", "base_price", "name"]},
        ),
    ]
