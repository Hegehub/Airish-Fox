# Generated manually for Airish Fox payments stage 6.

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="requires_manual_review",
            field=models.BooleanField(default=False, verbose_name="Требует ручной проверки"),
        ),
        migrations.AddField(
            model_name="order",
            name="manual_review_reason",
            field=models.TextField(blank=True, verbose_name="Причина ручной проверки"),
        ),
    ]
