# Generated manually for Airish Fox checkout stage 5.

import decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="PromoCode",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("code", models.CharField(max_length=50, unique=True, verbose_name="Код")),
                ("description", models.CharField(blank=True, max_length=255, verbose_name="Описание")),
                ("discount_type", models.CharField(choices=[("percent", "Percent"), ("fixed", "Fixed")], max_length=20, verbose_name="Тип скидки")),
                ("value", models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(decimal.Decimal("0"))], verbose_name="Значение")),
                ("is_active", models.BooleanField(default=True, verbose_name="Активен")),
                ("valid_from", models.DateTimeField(blank=True, null=True, verbose_name="Действует с")),
                ("valid_until", models.DateTimeField(blank=True, null=True, verbose_name="Действует до")),
                ("max_uses", models.PositiveIntegerField(blank=True, null=True, verbose_name="Максимум использований")),
                ("used_count", models.PositiveIntegerField(default=0, verbose_name="Использований")),
                ("minimum_order_amount", models.DecimalField(decimal_places=2, default=0, max_digits=12, validators=[django.core.validators.MinValueValidator(decimal.Decimal("0"))], verbose_name="Минимальная сумма")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Создан")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Обновлён")),
            ],
            options={"verbose_name": "Промокод", "verbose_name_plural": "Промокоды", "ordering": ["code"]},
        ),
    ]
