# Generated manually for Airish Fox store locator stage 7.

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("store_locator", "0001_initial"),
        ("orders", "0002_order_manual_review"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="pickup_store",
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="pickup_orders", to="store_locator.storelocation", verbose_name="Магазин самовывоза"),
        ),
        migrations.AddField(
            model_name="order",
            name="pickup_store_name",
            field=models.CharField(blank=True, max_length=160, verbose_name="Магазин самовывоза snapshot"),
        ),
        migrations.AddField(
            model_name="order",
            name="pickup_store_address",
            field=models.TextField(blank=True, verbose_name="Адрес самовывоза snapshot"),
        ),
    ]
