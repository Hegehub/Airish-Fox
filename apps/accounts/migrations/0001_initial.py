# Generated manually for Airish Fox accounts stage 3.

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
            name="CustomerProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("phone", models.CharField(blank=True, max_length=40, verbose_name="Телефон")),
                ("birthday", models.DateField(blank=True, null=True, verbose_name="Дата рождения")),
                ("preferred_size_top", models.CharField(blank=True, max_length=40, verbose_name="Размер верха")),
                ("preferred_size_bottom", models.CharField(blank=True, max_length=40, verbose_name="Размер низа")),
                ("preferred_fit", models.CharField(blank=True, choices=[("slim", "Slim"), ("regular", "Regular"), ("relaxed", "Relaxed"), ("oversized", "Oversized")], max_length=20, verbose_name="Посадка")),
                ("favorite_color", models.CharField(blank=True, max_length=80, verbose_name="Любимый цвет")),
                ("marketing_consent", models.BooleanField(default=False, verbose_name="Согласие на маркетинг")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Создан")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Обновлён")),
                ("favorite_mood", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="customer_profiles", to="catalog.moodcollection", verbose_name="Любимое настроение")),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="customer_profile", to=settings.AUTH_USER_MODEL, verbose_name="Пользователь")),
            ],
            options={"verbose_name": "Профиль покупателя", "verbose_name_plural": "Профили покупателей"},
        ),
        migrations.CreateModel(
            name="Address",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("full_name", models.CharField(max_length=160, verbose_name="Имя получателя")),
                ("phone", models.CharField(max_length=40, verbose_name="Телефон")),
                ("country", models.CharField(default="Vietnam", max_length=80, verbose_name="Страна")),
                ("city", models.CharField(max_length=120, verbose_name="Город")),
                ("district", models.CharField(blank=True, max_length=120, verbose_name="Район")),
                ("ward", models.CharField(blank=True, max_length=120, verbose_name="Ward")),
                ("street_address", models.TextField(verbose_name="Адрес")),
                ("postal_code", models.CharField(blank=True, max_length=40, verbose_name="Почтовый индекс")),
                ("delivery_notes", models.TextField(blank=True, verbose_name="Заметки для доставки")),
                ("is_default_shipping", models.BooleanField(default=False, verbose_name="Адрес доставки по умолчанию")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Создан")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Обновлён")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="addresses", to=settings.AUTH_USER_MODEL, verbose_name="Пользователь")),
            ],
            options={"verbose_name": "Адрес", "verbose_name_plural": "Адреса", "ordering": ["-is_default_shipping", "-updated_at"]},
        ),
    ]
