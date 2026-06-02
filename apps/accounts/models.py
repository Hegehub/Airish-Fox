"""Customer account models for Airish Fox."""

from django.contrib.auth.models import User
from django.db import models, transaction

from apps.catalog.models import MoodCollection


class CustomerProfile(models.Model):
    class Fit(models.TextChoices):
        SLIM = "slim", "Slim"
        REGULAR = "regular", "Regular"
        RELAXED = "relaxed", "Relaxed"
        OVERSIZED = "oversized", "Oversized"

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="customer_profile", verbose_name="Пользователь")
    phone = models.CharField("Телефон", max_length=40, blank=True)
    birthday = models.DateField("Дата рождения", blank=True, null=True)
    preferred_size_top = models.CharField("Размер верха", max_length=40, blank=True)
    preferred_size_bottom = models.CharField("Размер низа", max_length=40, blank=True)
    preferred_fit = models.CharField("Посадка", max_length=20, choices=Fit.choices, blank=True)
    favorite_color = models.CharField("Любимый цвет", max_length=80, blank=True)
    favorite_mood = models.ForeignKey(
        MoodCollection,
        on_delete=models.SET_NULL,
        related_name="customer_profiles",
        verbose_name="Любимое настроение",
        blank=True,
        null=True,
    )
    marketing_consent = models.BooleanField("Согласие на маркетинг", default=False)
    created_at = models.DateTimeField("Создан", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлён", auto_now=True)

    class Meta:
        verbose_name = "Профиль покупателя"
        verbose_name_plural = "Профили покупателей"

    def __str__(self):
        return f"Профиль {self.user.get_username()}"


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses", verbose_name="Пользователь")
    full_name = models.CharField("Имя получателя", max_length=160)
    phone = models.CharField("Телефон", max_length=40)
    country = models.CharField("Страна", max_length=80, default="Vietnam")
    city = models.CharField("Город", max_length=120)
    district = models.CharField("Район", max_length=120, blank=True)
    ward = models.CharField("Ward", max_length=120, blank=True)
    street_address = models.TextField("Адрес")
    postal_code = models.CharField("Почтовый индекс", max_length=40, blank=True)
    delivery_notes = models.TextField("Заметки для доставки", blank=True)
    is_default_shipping = models.BooleanField("Адрес доставки по умолчанию", default=False)
    created_at = models.DateTimeField("Создан", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлён", auto_now=True)

    class Meta:
        verbose_name = "Адрес"
        verbose_name_plural = "Адреса"
        ordering = ["-is_default_shipping", "-updated_at"]

    def __str__(self):
        return f"{self.full_name}, {self.city}"

    def save(self, *args, **kwargs):
        from .services import set_default_shipping_address

        with transaction.atomic():
            super().save(*args, **kwargs)
            set_default_shipping_address(self)
