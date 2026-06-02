# Generated manually for Airish Fox store locator stage 7.

import decimal
import django.core.validators
import django.db.models.deletion
from django.db import migrations, models

import apps.catalog.services


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="StoreLocation",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=160, verbose_name="Название")),
                ("slug", models.SlugField(unique=True, verbose_name="Slug")),
                ("short_description", models.CharField(blank=True, max_length=255, verbose_name="Короткое описание")),
                ("description", models.TextField(blank=True, verbose_name="Описание")),
                ("country", models.CharField(default="Vietnam", max_length=80, verbose_name="Страна")),
                ("city", models.CharField(max_length=120, verbose_name="Город")),
                ("district", models.CharField(blank=True, max_length=120, verbose_name="Район")),
                ("street_address", models.CharField(max_length=255, verbose_name="Улица и дом")),
                ("full_address", models.TextField(blank=True, verbose_name="Полный адрес")),
                ("latitude", models.DecimalField(decimal_places=7, max_digits=10, validators=[django.core.validators.MinValueValidator(decimal.Decimal("-90")), django.core.validators.MaxValueValidator(decimal.Decimal("90"))], verbose_name="Широта")),
                ("longitude", models.DecimalField(decimal_places=7, max_digits=10, validators=[django.core.validators.MinValueValidator(decimal.Decimal("-180")), django.core.validators.MaxValueValidator(decimal.Decimal("180"))], verbose_name="Долгота")),
                ("phone", models.CharField(blank=True, max_length=40, verbose_name="Телефон")),
                ("email", models.EmailField(blank=True, max_length=254, verbose_name="Email")),
                ("whatsapp_url", models.URLField(blank=True, verbose_name="WhatsApp")),
                ("telegram_url", models.URLField(blank=True, verbose_name="Telegram")),
                ("instagram_url", models.URLField(blank=True, verbose_name="Instagram")),
                ("google_maps_place_url", models.URLField(blank=True, verbose_name="Google Maps place URL")),
                ("google_maps_embed_url", models.URLField(blank=True, verbose_name="Google Maps embed URL")),
                ("is_active", models.BooleanField(default=True, verbose_name="Активен")),
                ("is_main_store", models.BooleanField(default=False, verbose_name="Главный магазин")),
                ("pickup_available", models.BooleanField(default=True, verbose_name="Самовывоз доступен")),
                ("fitting_available", models.BooleanField(default=True, verbose_name="Примерка доступна")),
                ("sort_order", models.PositiveIntegerField(default=0, verbose_name="Порядок")),
                ("image", models.ImageField(blank=True, null=True, upload_to="stores/", validators=[apps.catalog.services.validate_image_extension, apps.catalog.services.validate_image_size], verbose_name="Изображение")),
                ("seo_title", models.CharField(blank=True, max_length=255, verbose_name="SEO title")),
                ("seo_description", models.TextField(blank=True, verbose_name="SEO description")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Создан")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Обновлён")),
            ],
            options={"verbose_name": "Магазин", "verbose_name_plural": "Магазины", "ordering": ["sort_order", "name"]},
        ),
        migrations.CreateModel(
            name="StoreOpeningHour",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("weekday", models.PositiveSmallIntegerField(choices=[(0, "Monday"), (1, "Tuesday"), (2, "Wednesday"), (3, "Thursday"), (4, "Friday"), (5, "Saturday"), (6, "Sunday")], verbose_name="День недели")),
                ("opens_at", models.TimeField(blank=True, null=True, verbose_name="Открывается")),
                ("closes_at", models.TimeField(blank=True, null=True, verbose_name="Закрывается")),
                ("is_closed", models.BooleanField(default=False, verbose_name="Закрыто")),
                ("note", models.CharField(blank=True, max_length=160, verbose_name="Заметка")),
                ("store", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="opening_hours", to="store_locator.storelocation", verbose_name="Магазин")),
            ],
            options={"verbose_name": "Часы работы", "verbose_name_plural": "Часы работы", "ordering": ["weekday"], "unique_together": {("store", "weekday")}},
        ),
        migrations.CreateModel(
            name="StorePhoto",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("image", models.ImageField(upload_to="stores/gallery/", validators=[apps.catalog.services.validate_image_extension, apps.catalog.services.validate_image_size], verbose_name="Фото")),
                ("alt_text", models.CharField(blank=True, max_length=180, verbose_name="Alt text")),
                ("sort_order", models.PositiveIntegerField(default=0, verbose_name="Порядок")),
                ("store", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="photos", to="store_locator.storelocation", verbose_name="Магазин")),
            ],
            options={"verbose_name": "Фото магазина", "verbose_name_plural": "Фото магазина", "ordering": ["sort_order", "id"]},
        ),
    ]
